py-rodo aka py-rabbit-opensuse-org
==================================

This is a small helper library to process messages emitted to
`rabbit.opensuse.org <https://rabbit.opensuse.org/>`_ by the Open Build Service.


Usage
-----

.. warning::
   This library is experimental and is the product of trial & error
   experimentation. Proceed with caution.

Before importing any other ``py_rodo`` modules, you must configure the backend
by calling ``set_backend()``. This allows you to choose between different
dataclass implementations:

.. code-block:: python

   from py_rodo.config import Backend, set_backend

   # Choose your backend: Backend.DATACLASSY or Backend.PYDANTIC
   set_backend(Backend.PYDANTIC)

   # Now import other modules
   from py_rodo import QueueProcessor, RoutingKey
   from py_rodo.types import PackageCommitPayload

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

This package is available as a single package on PyPI. You choose your backend
at runtime by calling ``set_backend()`` before importing other ``py_rodo``
modules.

.. code-block:: bash

     pip install py-rodo

The package supports two backends:

- ``Backend.DATACLASSY``: Uses the `dataclassy` library
- ``Backend.PYDANTIC``: Uses Pydantic (automatically detects v1 or v2)

Both backends work with Python 3.10+. When using the Pydantic backend, you can
use either Pydantic v1 (``pydantic<2``) or Pydantic v2 (``pydantic>=2``).

After installation, remember to set the backend before importing other modules:

.. code-block:: python

     from py_rodo.config import Backend, set_backend
     set_backend(Backend.PYDANTIC)  # or Backend.DATACLASSY

     from py_rodo import QueueProcessor


Development and Testing
-----------------------

For local development, install the package in editable mode with your preferred
backend dependencies:

.. code-block:: bash

     # Install with pydantic backend
     pip install -e ".[pydantic]"

     # Or with dataclassy backend
     pip install -e ".[dataclassy]"

For testing, use tox to test against multiple Python versions and backends:

.. code-block:: bash

     # Run tests for specific backend and Python version
     tox -e test-py311-pydantic-v1
     tox -e test-py312-pydantic-v2
     tox -e test-py313-dataclassy

     # Run type checking for different backends
     tox -e mypy-pydantic-v1
     tox -e mypy-pydantic-v2
     tox -e mypy-dataclassy

     # Run formatting check
     tox -e format

     # Run linting
     tox -e lint

     # Launch editor with configured environment
     tox -e devel-pydantic-v2 -- code .
     tox -e devel-dataclassy -- emacs &

To test both Pydantic v1 and v2 with the same Python version, use the different
tox environments:

.. code-block:: bash

     # Test both pydantic versions with Python 3.12
     tox -e test-py312-pydantic-v1
     tox -e test-py312-pydantic-v2
     tox -e test-py312-dataclassy
