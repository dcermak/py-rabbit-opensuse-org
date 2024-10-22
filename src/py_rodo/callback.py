import json
import logging
from typing import Callable
from typing import Dict

import pika
import pika.exceptions
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic

from py_rodo.types import QUEUE_TO_PAYLOAD_TYPE
from py_rodo.types import ObsMessageBusPayloadBase
from py_rodo.types import RoutingKey

_PREFIX = "opensuse.obs."


def listen_forever(
    callbacks: Dict[RoutingKey, Callable[[ObsMessageBusPayloadBase], None]],
    *,
    error_on_unknown_routing_keys: bool = False,
    logger: logging.Logger | None = None,
    invalid_payload_is_fatal: bool = True,
) -> None:
    def callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: pika.BasicProperties,
        body: bytes,
    ) -> None:
        rt = method.routing_key or ""

        if logger:
            logger.debug("Routing key: %s", rt)

        if not rt.startswith(_PREFIX) or rt == f"{_PREFIX}metrics":
            if logger:
                logger.debug(
                    "Skipping message with routing key '%s', invalid prefix or metrics key",
                    rt,
                )
            return None

        try:
            routing_key = RoutingKey(rt.removeprefix(_PREFIX))
        except ValueError as val_err:
            if error_on_unknown_routing_keys:
                raise RuntimeError(f"Invalid routing key {rt}") from val_err

            return None

        if routing_key not in callbacks:
            if logger:
                logger.debug(
                    "Skipping message with routing key '%s', not in callbacks", rt
                )
            return None

        payload_type = QUEUE_TO_PAYLOAD_TYPE[routing_key]
        if logger:
            logger.debug("Inferred payload type %s", payload_type)

        try:
            kwargs = json.loads(body.decode())
            if logger:
                logger.debug("Raw message payload: %s", kwargs)

            payload = payload_type(**kwargs)
        except TypeError as type_err:
            if invalid_payload_is_fatal:
                raise

            if logger:
                logger.error(
                    "Failed to process message body: %s\nGot %s",
                    body.decode(),
                    type_err,
                )
            return None

        callbacks[routing_key](payload)

    while True:
        connection: pika.BlockingConnection | None = None
        channel: BlockingChannel | None = None
        try:
            connection = pika.BlockingConnection(
                pika.URLParameters("amqps://opensuse:opensuse@rabbit.opensuse.org")
            )
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

            channel.basic_consume(queue_name, callback, auto_ack=True)

            channel.start_consuming()

        except pika.exceptions.ConnectionClosedByBroker:
            if logger:
                logger.debug("Broker closed connection, retrying")
            continue

        except pika.exceptions.AMQPChannelError as err:
            # Do not recover on channel errors
            if logger:
                logger.error("Caught a channel error: %s, stopping!", err)
            break

        except pika.exceptions.AMQPConnectionError as err:
            # Recover on all other connection errors
            if logger:
                logger.debug("Connection was closed: %s, retrying", err)
            continue


def try_listening() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(message)s"))

    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(handler)

    callbacks = {}
    for rt in RoutingKey:

        def cb(payload) -> None:
            pass

        callbacks[rt] = cb

    listen_forever(callbacks, error_on_unknown_routing_keys=True, logger=LOGGER)
