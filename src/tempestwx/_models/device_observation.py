"""StationObservation model."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import ConfigDict, Field

from ._serializer import Model
from .device_observation_summary import DeviceObservationSummary
from .status import Status


class DeviceObservation(Model):
    status: Optional[Status] = None  # object
    device_id: Optional[int] = None  # int32
    type_: Optional[str] = Field(None, alias="type")  # string
    source: Optional[str] = None  # string
    summary: Optional[DeviceObservationSummary] = None  # object
    bucket_step_minutes: Optional[Union[float, int]] = None  # number

    # An array of observation value-arrays (aligned to obs_fields order)
    obs: Optional[List[List[Union[float, int, str, None]]]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["DeviceObservation"]
