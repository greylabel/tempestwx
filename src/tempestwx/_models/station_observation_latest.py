"""StationObservation model."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .observation import Observation
from .station_units import StationUnits
from .status import Status


class StationObservationLatest(Model):
    station_id: Optional[int] = None  # int32
    station_name: Optional[str] = None  # string
    public_name: Optional[str] = None  # string
    latitude: Optional[Union[float, int]] = None  # float
    longitude: Optional[Union[float, int]] = None  # float
    timezone: Optional[str] = None  # string
    elevation: Optional[Union[float, int]] = None  # float
    is_public: Optional[bool] = None  # boolean
    status: Optional[Status] = None  # object
    station_units: Optional[StationUnits] = None  # object
    outdoor_keys: Optional[List[str]] = None  # array of strings
    obs: Optional[List[Observation]] = None  # array of observations

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["StationObservationLatest"]
