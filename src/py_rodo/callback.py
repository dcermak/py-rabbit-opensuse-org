"""This module contains the main entry point: the :py:class:`QueueProcessor`
class. It provides a method to listen to the event bus and invoke user defined
callbacks for specific message types.

"""

import json
import logging
from typing import Callable
from typing import Dict
from typing import Type

import pika
import pika.exceptions
from dataclassy import dataclass
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic

from py_rodo.types import QUEUE_TO_PAYLOAD_TYPE
from py_rodo.types import ObsMessageBusPayloadBase
from py_rodo.types import RoutingKey


@dataclass(frozen=True, kw_only=True)
class QueueProcessor:
    #: routing key prefix defined by the build service instance as the
    #: ``amqp_namespace`` setting, see
    #: https://openbuildservice.org/help/manuals/obs-admin-guide/obs-cha-administration#message-bus-rabbit-mq-rabbit-mq-configuration
    prefix: str = "opensuse.obs."

    #: URL to the amqp queue
    queue_url: str = "amqps://opensuse:opensuse@rabbit.opensuse.org"

    #: Optional logger for debug & error logging
    logger: logging.Logger | None = None

    #: Dictionary of callback functions that are invoked by
    #: :py:meth:`~listen_forever`.
    #:
    #: The dictionary allows to specify a callback function for each routing
    #: key. The callback function then receives the deserialized payload as an
    #: instance of the corresponding child class of
    #: :py:class:`~py_rodo.types.ObsMessageBusPayloadBase`.
    callbacks: Dict[RoutingKey, Callable[[ObsMessageBusPayloadBase], None]]

    def __post_init__(self) -> None:
        if not self.prefix.endswith("."):
            raise ValueError(
                f"message routing key prefix must end with a dot, got {self.prefix}"
            )

    def invalid_routing_key_callback(
        self, routing_key: str, body: bytes, val_err: ValueError
    ) -> None:
        """Callback function that is invoked if a message is received with a
        ``routing_key`` that is not in :py:class:`~py_rodo.types.RoutingKey`.

        This implementation only logs the error.
        """
        if self.logger:
            self.logger.error(
                "Got error %s\nInvalid routing key '%s' with body: %s",
                val_err,
                routing_key,
                body.decode(),
            )

    def invalid_payload_callback(
        self,
        body: bytes,
        type_err: TypeError,
        child_cls: Type[ObsMessageBusPayloadBase],
        routing_key: RoutingKey,
    ) -> None:
        """Callback that is invoked if the construction of a child class of
        :py:class:`~py_rodo.types.ObsMessageBusPayloadBase` from the message
        body failed.

        This implementation only logs the error.

        """
        if self.logger:
            self.logger.error(
                "Failed to construct an instance of %s for the routing key %s from '%s'. Received error: %s",
                child_cls,
                routing_key,
                body.decode(),
                type_err,
            )

    def listen_forever(self) -> None:
        while True:
            connection: pika.BlockingConnection | None = None
            channel: BlockingChannel | None = None
            try:
                connection = pika.BlockingConnection(pika.URLParameters(self.queue_url))
                channel = connection.channel()

                channel.exchange_declare(
                    exchange="pubsub",
                    exchange_type=ExchangeType.topic,
                    passive=True,
                    durable=True,
                )

                result = channel.queue_declare("", exclusive=True)
                queue_name = result.method.queue
                assert queue_name

                channel.queue_bind(exchange="pubsub", queue=queue_name, routing_key="#")

                channel.basic_consume(
                    queue_name, self._single_message_callback, auto_ack=True
                )

                channel.start_consuming()

            except pika.exceptions.ConnectionClosedByBroker:
                if self.logger:
                    self.logger.debug("Broker closed connection, retrying")
                continue

            except pika.exceptions.AMQPChannelError as err:
                # Do not recover on channel errors
                if self.logger:
                    self.logger.error("Caught a channel error: %s, stopping!", err)
                break

            except pika.exceptions.AMQPConnectionError as err:
                # Recover on all other connection errors
                if self.logger:
                    self.logger.debug("Connection was closed: %s, retrying", err)
                continue

    def _single_message_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: pika.BasicProperties,
        body: bytes,
    ) -> None:
        """Callback that processes a single AMQP message."""
        rt = method.routing_key or ""

        if self.logger:
            self.logger.debug("Routing key: %s", rt)

        if not rt.startswith(self.prefix) or rt == f"{self.prefix}metrics":
            if self.logger:
                self.logger.debug(
                    "Skipping message with routing key '%s', invalid prefix or metrics key",
                    rt,
                )
            return None

        try:
            routing_key = RoutingKey(rt.removeprefix(self.prefix))
        except ValueError as val_err:
            self.invalid_routing_key_callback(rt, body, val_err)
            return

        if routing_key not in self.callbacks:
            if self.logger:
                self.logger.debug(
                    "Skipping message with routing key '%s', not in callbacks", rt
                )
            return None

        payload_type = QUEUE_TO_PAYLOAD_TYPE[routing_key]
        if self.logger:
            self.logger.debug("Inferred payload type %s", payload_type)

        try:
            kwargs = json.loads(body.decode())
            if self.logger:
                self.logger.debug("Raw message payload: %s", kwargs)

            payload = payload_type(**kwargs)
        except TypeError as type_err:
            self.invalid_payload_callback(body, type_err, payload_type, routing_key)
            return None

        self.callbacks[routing_key](payload)


def try_listening() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance",
        "-i",
        nargs=1,
        choices=["obs", "ibs"],
        default=["obs"],
        help="AMQP instance to connect to",
    )
    parser.add_argument(
        "--verbose", "-v", action="count", help="configure the logging verbosity"
    )

    _LOG_LEVELS = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]

    args = parser.parse_args()

    log_level = _LOG_LEVELS[min(args.verbose or 0, len(_LOG_LEVELS) - 1)]

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(message)s"))

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    if args.instance[0] == "obs":
        prefix = "opensuse.obs."
        queue_url = "amqps://opensuse:opensuse@rabbit.opensuse.org"
    elif args.instance[0] == "ibs":
        prefix = "suse.obs."
        queue_url = "amqps://suse:suse@rabbit.suse.de"
    else:
        raise ValueError(f"Invalid instance {args.instance[0]}")

    callbacks = {}
    for rt in RoutingKey:

        def build_callback(
            routing_key: RoutingKey,
        ) -> Callable[[ObsMessageBusPayloadBase], None]:
            def cb(payload: ObsMessageBusPayloadBase) -> None:
                assert isinstance(
                    payload, (tp := QUEUE_TO_PAYLOAD_TYPE[routing_key])
                ), f"expected {payload} to have type {tp}, but got {type(payload)}"

            return cb

        callbacks[rt] = build_callback(rt)

    class HardFailureListener(QueueProcessor):
        def invalid_payload_callback(
            self,
            body: bytes,
            type_err: TypeError,
            child_cls: Type[ObsMessageBusPayloadBase],
            routing_key: RoutingKey,
        ) -> None:
            super().invalid_payload_callback(body, type_err, child_cls, routing_key)
            raise type_err

        def invalid_routing_key_callback(
            self, routing_key: str, body: bytes, val_err: ValueError
        ) -> None:
            super().invalid_routing_key_callback(routing_key, body, val_err)
            raise val_err

    listener = HardFailureListener(
        callbacks=callbacks, logger=logger, prefix=prefix, queue_url=queue_url
    )
    listener.listen_forever()
