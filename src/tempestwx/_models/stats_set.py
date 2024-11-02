"""StatsSet model"""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict, Field

from tempestwx._models.status import Status

from ._serializer import Model


class StatsSet(Model):
    status: Optional[Status] = None  # object
    station_id: Optional[int] = None  # int32
    type_: Optional[str] = Field(None, alias="type")  # string
    first_ob_local_day: Optional[str] = None  # string
    last_ob_local_day: Optional[str] = None  # string
    stats_day: Optional[list[list[Union[str, int, float, None]]]] = None  # array of arrays

    # Omitted from docs but present in API
    stats_week: Optional[list[list[Union[str, int, float, None]]]] = (
        None  # array of arrays of string | int32 | float | null
    )
    stats_month: Optional[list[list[Union[str, int, float, None]]]] = (
        None  # array of arrays of string | int32 | float | null
    )
    stats_year: Optional[list[list[Union[str, int, float, None]]]] = (
        None  # array of arrays of string | int32 | float | null
    )
    stats_alltime: Optional[list[Union[str, int, float, None]]] = (
        None  # array of string | int32 | float | null
    )
    stats_week_time: Optional[list[list[Union[str, None]]]] = (
        None  # array of arrays of strings | nulls
    )
    stats_month_time: Optional[list[list[Union[str, None]]]] = (
        None  # array of arrays of strings | nulls
    )
    stats_year_time: Optional[list[list[Union[str, None]]]] = (
        None  # array of arrays of strings | nulls
    )
    stats_alltime_time: Optional[list[Union[str, None]]] = None  # array of strings | nulls
    last_ob_day_local: Optional[str] = None  # string
    first_ob_day_local: Optional[str] = None  # string

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["StatsSet"]
