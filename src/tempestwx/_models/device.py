"""Device model with DeviceType enum."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict

from ._serializer import Model, StrEnum
from .device_meta import DeviceMeta
from .device_settings import DeviceSettings


class DeviceType(StrEnum):
    HB = "HB"
    AR = "AR"
    SK = "SK"
    ST = "ST"


class Device(Model):
    device_id: Optional[int] = None  # int32
    serial_number: Optional[str] = None  # string
    device_meta: Optional[DeviceMeta] = None
    device_settings: Optional[DeviceSettings] = None
    device_type: Optional[DeviceType] = None  # string enum
    hardware_revision: Optional[str] = None  # string
    firmware_revision: Optional[str] = None  # string
    notes: Optional[str] = None  # string

    location_id: Optional[int] = None  # int32

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["Device", "DeviceType"]
