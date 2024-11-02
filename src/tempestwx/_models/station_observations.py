"""StationObservation model."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import ConfigDict, Field

from ._serializer import Model
from .station_units import StationUnits
from .status import Status


class StationObservation(Model):
    station_id: Optional[int] = None  # int32
    type_: Optional[str] = Field(None, alias="type")  # string
    ob_fields: Optional[List[str]] = None  # array
    status: Optional[Status] = None  # object
    source: Optional[str] = None  # string
    units: Optional[StationUnits] = None  # object
    timezone: Optional[str] = None  # string

    # An array of observation value-arrays (aligned to obs_fields order)
    obs: Optional[List[List[Union[float, int, str, None]]]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["StationObservation"]
