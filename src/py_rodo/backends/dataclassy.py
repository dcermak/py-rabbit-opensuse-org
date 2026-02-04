"""Dataclassy backend implementation."""

from dataclassy import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class ObsMessageBusPayloadBase:
    """Base class for all OBS message bus payload types.

    This class is a frozen dataclassy dataclass.
    """

    pass
