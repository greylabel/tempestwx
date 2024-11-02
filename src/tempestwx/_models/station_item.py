"""StationItem model."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict

from ._serializer import Model


class StationItem(Model):
    location_item_id: Optional[int] = None  # int32
    location_id: Optional[int] = None  # int32
    device_id: Optional[int] = None  # int32
    item: Optional[str] = None  # string
    sort: Optional[int] = None  # number
    station_id: Optional[int] = None  # int32
    station_item_id: Optional[int] = None  # int32

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["StationItem"]
