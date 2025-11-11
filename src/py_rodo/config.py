"""Backend configuration for py_rodo.

Users must call set_backend() before importing other py_rodo modules.
"""

from enum import Enum
from enum import unique
from typing import Type


@unique
class Backend(str, Enum):
    """Enum for available py_rodo backends"""

    DATACLASSY = "dataclassy"
    PYDANTIC = "pydantic"

    def __str__(self) -> str:
        return self.value


_backend: Backend | None = None


def set_backend(backend: Backend | str) -> None:
    """Set the backend for py_rodo message payload classes.

    Must be called before importing py_rodo payload types.

    Args:
        backend: Either a Backend enum value or a string ('dataclassy' or 'pydantic')

    Raises:
        ValueError: If an invalid backend is specified
    """
    global _backend

    if isinstance(backend, str):
        try:
            backend = Backend(backend)
        except ValueError:
            valid_backends = ", ".join(b.value for b in Backend)
            raise ValueError(
                f"Invalid backend: {backend}. Must be one of: {valid_backends}"
            ) from None
    elif not isinstance(backend, Backend):
        raise TypeError(f"backend must be Backend enum or string, got {type(backend)}")

    _backend = backend


def _get_backend() -> Backend:
    """Get the currently configured backend.

    Returns:
        The Backend enum value, or raises an error if not set.

    Raises:
        RuntimeError: If set_backend() has not been called yet
    """
    if _backend is None:
        raise RuntimeError(
            "Backend not configured. Call py_rodo.config.set_backend() before "
            "importing py_rodo modules. Valid values: Backend.DATACLASSY, "
            "Backend.PYDANTIC"
        )
    return _backend


def get_base_class() -> Type:
    """Get the appropriate ObsMessageBusPayloadBase class for the configured backend.

    Returns:
        The backend-specific base class for all payload types
    """
    backend = _get_backend()

    if backend == Backend.DATACLASSY:
        from .backends.dataclassy import (  # type: ignore[assignment]
            ObsMessageBusPayloadBase,
        )

        return ObsMessageBusPayloadBase
    if backend == Backend.PYDANTIC:
        from .backends.pydantic import (  # type: ignore[assignment]
            ObsMessageBusPayloadBase,
        )

        return ObsMessageBusPayloadBase

    raise ValueError(f"Unknown backend: {backend}")
