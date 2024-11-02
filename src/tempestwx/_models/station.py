"""Station model."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import ConfigDict

from ._serializer import Model, StrEnum
from .device import Device
from .station_item import StationItem
from .station_meta import StationMeta
from .units_default import Environment


class StationCapability(StrEnum):
    air_temperature_humidity = "air_temperature_humidity"
    barometric_pressure = "barometric_pressure"
    light = "light"
    lightning = "lightning"
    rain = "rain"
    wind = "wind"


class StationCapabilities(Model):
    device_id: Optional[int] = None  # int32
    capability: Optional[StationCapability] = None  # string enum
    agl: Optional[Union[float, int]] = None  # float
    environment: Optional[Environment] = None  # string enum
    show_precip_final: Optional[bool] = None  # boolean


class Station(Model):
    location_id: Optional[int] = None  # int32
    station_id: Optional[int] = None  # int32
    name: Optional[str] = None  # string
    public_name: Optional[str] = None  # string
    latitude: Optional[Union[float, int]] = None  # float
    longitude: Optional[Union[float, int]] = None  # float
    timezone: Optional[str] = None  # string
    timezone_offset_minutes: Optional[Union[float, int]] = None  # number
    station_meta: Optional[StationMeta] = None  # object
    last_modified_epoch: Optional[int] = None  # number
    created_epoch: Optional[int] = None  # number
    devices: Optional[List[Device]] = None  # array of objects
    station_items: Optional[List[StationItem]] = None  # array of objects
    is_local_mode: Optional[bool] = None  # boolean

    # Omitted from docs but present in API
    capabilities: Optional[List[StationCapabilities]] = None  # array of objects
    state: Optional[int] = None  # boolean

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["Station", "StationCapabilities", "StationCapability"]
