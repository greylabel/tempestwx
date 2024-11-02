"""StationObservationValues model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model, StrEnum


class ObservationType(StrEnum):
    obs_st = "obs_st"
    obs_sky = "obs_sky"
    obs_air = "obs_air"
    obs_st_ext = "obs_st_ext"
    obs_air_ext = "obs_air_ext"
    obs_sky_ext = "obs_sky_ext"
    evt_strike = "evt_strike"
    rapid_wind = "rapid_wind"


class Observation(Model):
    timestamp: Optional[Union[float, int]] = None  # number
    air_temperature: Optional[Union[float, int]] = None  # float
    barometric_pressure: Optional[Union[float, int]] = None  # float
    station_pressure: Optional[Union[float, int]] = None  # float
    sea_level_pressure: Optional[Union[float, int]] = None  # float`
    relative_humidity: Optional[Union[float, int]] = None  # number
    precip: Optional[Union[float, int]] = None  # float
    precip_accum_last_1hr: Optional[Union[float, int]] = None  # float
    precip_accum_local_day: Optional[Union[float, int]] = None  # float
    precip_accum_local_day_final: Optional[Union[float, int]] = None  # float
    precip_accum_local_yesterday: Optional[Union[float, int]] = None  # float
    precip_accum_local_yesterday_final: Optional[Union[float, int]] = None
    precip_minutes_local_day: Optional[Union[float, int]] = None  # number
    precip_minutes_local_yesterday: Optional[Union[float, int]] = None  # number
    precip_minutes_local_yesterday_final: Optional[Union[float, int]] = None  # number
    precip_analysis_type_yesterday: Optional[Union[float, int]] = None  # number
    wind_avg: Optional[Union[float, int]] = None  # float
    wind_direction: Optional[Union[float, int]] = None  # number
    wind_gust: Optional[Union[float, int]] = None  # float
    wind_lull: Optional[Union[float, int]] = None  # float
    solar_radiation: Optional[Union[float, int]] = None  # number
    uv: Optional[Union[float, int]] = None  # number
    brightness: Optional[Union[float, int]] = None  # number
    lightning_strike_last_epoch: Optional[Union[float, int]] = None  # number
    lightning_strike_last_distance: Optional[Union[float, int]] = None  # number
    lightning_strike_count: Optional[Union[float, int]] = None  # number
    lightning_strike_count_last_1hr: Optional[Union[float, int]] = None  # number
    lightning_strike_count_last_3hr: Optional[Union[float, int]] = None  # number
    feels_like: Optional[Union[float, int]] = None  # float
    heat_index: Optional[Union[float, int]] = None  # float
    wind_chill: Optional[Union[float, int]] = None  # float
    dew_point: Optional[Union[float, int]] = None  # float
    wet_bulb_temperature: Optional[Union[float, int]] = None  # float
    wet_bulb_globe_temperature: Optional[Union[float, int]] = None  # float
    delta_t: Optional[Union[float, int]] = None  # float
    air_density: Optional[Union[float, int]] = None  # float
    pressure_trend: Optional[str] = None  # string

    # air_temperature_indoor: Optional[Union[float, int]] = None
    # barometric_pressure_indoor: Optional[Union[float, int]] = None
    # sea_level_pressure_indoor: Optional[Union[float, int]] = None
    # relative_humidity_indoor: Optional[Union[float, int]] = None
    # precip_indoor: Optional[Union[float, int]] = None
    # precip_accum_last_1hr_indoor: Optional[Union[float, int]] = None
    # wind_avg_indoor: Optional[Union[float, int]] = None
    # wind_direction_indoor: Optional[Union[float, int]] = None
    # wind_gust_indoor: Optional[Union[float, int]] = None
    # wind_lull_indoor: Optional[Union[float, int]] = None
    # solar_radiation_indoor: Optional[Union[float, int]] = None
    # uv_indoor: Optional[Union[float, int]] = None
    # brightness_indoor: Optional[Union[float, int]] = None
    # lightning_strike_last_epoch_indoor: Optional[Union[float, int]] = None
    # lightning_strike_last_distance_indoor: Optional[Union[float, int]] = None
    # lightning_strike_count_last_3hr_indoor: Optional[Union[float, int]] = None
    # feels_like_indoor: Optional[Union[float, int]] = None
    # heat_index_indoor: Optional[Union[float, int]] = None
    # wind_chill_indoor: Optional[Union[float, int]] = None
    # dew_point_indoor: Optional[Union[float, int]] = None
    # wet_bulb_temperature_indoor: Optional[Union[float, int]] = None
    # delta_t_indoor: Optional[Union[float, int]] = None
    # air_density_indoor: Optional[Union[float, int]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        strict=True,
    )


__all__ = ["Observation", "ObservationType"]
