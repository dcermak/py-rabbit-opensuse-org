"""Pydantic backend implementation with automatic version detection."""

from typing import TYPE_CHECKING

import pydantic
from pydantic import BaseModel

_pydantic_major_version = int(pydantic.__version__.split(".")[0])

if _pydantic_major_version >= 2 or TYPE_CHECKING:
    from pydantic import ConfigDict

    class ObsMessageBusPayloadBase(BaseModel):
        """Base class for all OBS message bus payload types.

        This class is a pydantic BaseModel with a pydantic v2 compatible
        ``model_config``.
        """

        model_config = ConfigDict(frozen=True, extra="forbid")
else:

    class ObsMessageBusPayloadBase(BaseModel):
        """Base class for all OBS message bus payload types.

        This class is a pydantic BaseModel with a pydantic v1 compatible
        configuration class.
        """

        class Config:
            frozen = True
            extra = "forbid"
