"""BetterForecastDailyForecast model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .units_default import Conditions, Icon, PrecipIcon, PrecipType


class BetterForecastDailyForecast(Model):
    day_start_local: Optional[Union[float, int]] = None  # number
    day_num: Optional[Union[float, int]] = None  # number
    month_num: Optional[Union[float, int]] = None  # number
    conditions: Optional[Conditions] = None  # string enum
    icon: Optional[Icon] = None  # string enum
    sunrise: Optional[Union[float, int]] = None  # number
    sunset: Optional[Union[float, int]] = None  # number
    air_temp_high: Optional[Union[float, int]] = None  # number
    air_temp_low: Optional[Union[float, int]] = None  # number
    air_temp_high_color: Optional[str] = None  # string
    air_temp_low_color: Optional[str] = None  # string
    precip_probability: Optional[Union[float, int]] = None
    precip_icon: Optional[PrecipIcon] = None  # string enum
    precip_type: Optional[PrecipType] = None  # string enum

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = [
    "BetterForecastDailyForecast",
]
