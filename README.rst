py-rodo aka py-rabbit-opensuse-org
==================================

This is a small helper library to process messages emitted to
`rabbit.opensuse.org <https://rabbit.opensuse.org/>`_ by the Open Build Service.


Usage
-----

.. warning::
   This library is experimental and is the product of trial & error
   experimentation. Proceed with caution.

The main entry point for this library is the `QueueProcessor` class, which
listens to the message bus, processes messages and invokes user defined
callbacks depending on the message routing keys.

The message callback functions receive a child class of
`ObsMessageBusPayloadBase` as the single argument and should return nothing. The
specific subtype of `ObsMessageBusPayloadBase` can be infered from the
dictionary `QUEUE_TO_PAYLOAD_TYPE` which maps the routing keys to specific
payload types.

To only process package commit messages, create the following callback:

.. code-block:: python

   def commit_to_my_package(payload: PackageCommitPayload) -> None:
       # process the payload here

   callbacks = {RoutingKey.PACKAGE_COMMIT: commit_to_my_package}

   qp = QueueProcessor(callbacks=callbacks)
   qp.listen_forever()
