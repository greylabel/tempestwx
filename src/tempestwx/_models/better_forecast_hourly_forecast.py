"""BetterForecastHourlyForecast model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .units_default import Conditions, Icon, PrecipIcon, PrecipType


class BetterForecastHourlyForecast(Model):
    time: Optional[Union[float, int]] = None  # number
    conditions: Optional[Conditions] = None  # string enum
    icon: Optional[Icon] = None  # string enum
    air_temperature: Optional[Union[float, int]] = None  # number
    sea_level_pressure: Optional[Union[float, int]] = None  # float
    relative_humidity: Optional[Union[float, int]] = None  # number
    precip: Optional[Union[float, int]] = None  # float
    precip_probability: Optional[Union[float, int]] = None  # number
    precip_icon: Optional[PrecipIcon] = None  # string enum
    wind_avg: Optional[Union[float, int]] = None  # number
    wind_avg_color: Optional[str] = None  # string
    wind_direction: Optional[Union[float, int]] = None  # number
    wind_direction_cardinal: Optional[str] = None  # string
    wind_direction_icon: Optional[str] = None  # string
    wind_gust: Optional[Union[float, int]] = None  # number
    wind_gust_color: Optional[str] = None  # string
    uv: Optional[Union[float, int]] = None  # number
    feels_like: Optional[Union[float, int]] = None  # number
    local_hour: Optional[Union[float, int]] = None  # number
    local_day: Optional[Union[float, int]] = None  # number

    # Omitted from docs but present in API
    station_pressure: Optional[Union[float, int]] = None  # float
    precip_type: Optional[PrecipType] = None  # string

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["BetterForecastHourlyForecast"]
