"""BetterForecastCurrentConditions model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .units_default import Conditions, Icon, PressureTrend


class BetterForecastCurrentConditions(Model):
    time: Optional[Union[float, int]] = None  # number
    conditions: Optional[Conditions] = None
    icon: Optional[Icon] = None
    air_temperature: Optional[Union[float, int]] = None  # number
    sea_level_pressure: Optional[Union[float, int]] = None  # float
    station_pressure: Optional[Union[float, int]] = None  # float
    pressure_trend: Optional[PressureTrend] = None  # string enum
    relative_humidity: Optional[Union[float, int]] = None  # number
    wind_avg: Optional[Union[float, int]] = None  # number
    wind_direction: Optional[Union[float, int]] = None  # number
    wind_direction_cardinal: Optional[str] = None  # string
    wind_direction_icon: Optional[str] = None  # string
    wind_gust: Optional[Union[float, int]] = None  # number
    solar_radiation: Optional[Union[float, int]] = None  # number
    uv: Optional[Union[float, int]] = None  # number
    brightness: Optional[Union[float, int]] = None  # number
    feels_like: Optional[Union[float, int]] = None  # number
    dew_point: Optional[Union[float, int]] = None  # number
    wet_bulb_temperature: Optional[Union[float, int]] = None  # number
    wet_bulb_globe_temperature: Optional[Union[float, int]] = None  # number
    delta_t: Optional[Union[float, int]] = None  # number
    air_density: Optional[Union[float, int]] = None  # float
    lightning_strike_count_last_1hr: Optional[Union[float, int]] = None  # number
    lightning_strike_count_last_3hr: Optional[Union[float, int]] = None  # number
    lightning_strike_last_distance: Optional[Union[float, int]] = None  # number
    lightning_strike_last_distance_msg: Optional[str] = None  # string
    lightning_strike_last_epoch: Optional[Union[float, int]] = None  # number
    precip_accum_local_day: Optional[Union[float, int]] = None  # float
    precip_accum_local_yesterday: Optional[Union[float, int]] = None  # float
    precip_minutes_local_day: Optional[Union[float, int]] = None  # number
    precip_minutes_local_yesterday: Optional[Union[float, int]] = None  # number
    is_precip_local_day_rain_check: Optional[bool] = None  # boolean
    is_precip_local_yesterday_rain_check: Optional[bool] = None  # boolean

    # Omitted from docs but present in API
    precip_probability: Optional[Union[float, int]] = None  # number

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = [
    "BetterForecastCurrentConditions",
]
