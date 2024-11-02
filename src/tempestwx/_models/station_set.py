"""StationSet model."""

from __future__ import annotations

from typing import List, Optional

from pydantic import ConfigDict

from ._serializer import Model
from .station import Station
from .status import Status


class StationSet(Model):
    status: Optional[Status] = None  # object
    stations: Optional[List[Station]] = None  # array of objects

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        strict=True,
    )


__all__ = ["StationSet"]
