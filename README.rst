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


Installation
------------

This package is available in three variants on PyPI, one for each backend. All
three provide the same ``py_rodo`` module but use different payload class
implementations.

Available packages:

- ``py-rodo-dataclassy``: Uses the `dataclassy` library. Compatible with Python <=3.13
- ``py-rodo-pydantic-v1``: Uses Pydantic v1. Compatible with Python <= 3.13
- ``py-rodo-pydantic-v2``: Uses Pydantic v2. Compatible with Python 3.10-3.14

Install the variant you prefer:

.. code-block:: bash

    pip install py-rodo-dataclassy
    pip install py-rodo-pydantic-v1
    pip install py-rodo-pydantic-v2

All three packages import as ``py_rodo``:

.. code-block:: python

    import py_rodo
    from py_rodo import QueueProcessor


Building from Source
--------------------

To build a specific variant from source, set the ``PY_RODO_BACKEND`` environment
variable before building:

.. code-block:: bash

    # Build py-rodo-dataclassy
    PY_RODO_BACKEND=dataclassy python -m build

    # Build py-rodo-pydantic-v1
    PY_RODO_BACKEND=pydantic-v1 python -m build

    # Build py-rodo-pydantic-v2
    PY_RODO_BACKEND=pydantic-v2 python -m build

Each command generates a wheel with a different package name but the same module
name (``py_rodo``). The backend library is included as a required dependency.


Development and Testing
-----------------------

For local development, use tox development environments:

.. code-block:: bash

    # Recommended: Use tox to launch your editor with backend configured
    tox -e devel-pydantic-v2 -- emacs &
    tox -e devel-dataclassy -- code .

    # Alternative: Manual backend generation and install
    python scripts/generate_backend.py dataclassy
    pip install -e .[dataclassy]

To run tests with tox:

.. code-block:: bash

    # Run tests for specific backend and Python version
    tox -e test-py311-pydantic-v2

    # Run type checking
    tox -e mypy-dataclassy

    # Run formatting check
    tox -e format

    # Run linting
    tox -e lint-pydantic-v2
