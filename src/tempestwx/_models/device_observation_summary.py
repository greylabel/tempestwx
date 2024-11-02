"""StationObservation model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model


class DeviceObservationSummary(Model):
    pressure_trend: Optional[str] = None  # string
    strike_count_1h: Optional[Union[float, int]] = None  # number
    strike_count_3h: Optional[Union[float, int]] = None  # number
    precip_total_1h: Optional[Union[float, int]] = None  # number
    strike_last_dist: Optional[Union[float, int]] = None  # number
    strike_last_epoch: Optional[Union[float, int]] = None  # number
    precip_accum_local_yesterday: Optional[Union[float, int]] = None  # number
    precip_accum_local_yesterday_final: Optional[Union[float, int]] = None  # number
    precip_analysis_type_yesterday: Optional[Union[float, int]] = None  # number
    feels_like: Optional[Union[float, int]] = None  # number
    heat_index: Optional[Union[float, int]] = None  # number
    wind_chill: Optional[Union[float, int]] = None  # number
    dew_point: Optional[Union[float, int]] = None  # number
    wet_bulb_temperature: Optional[Union[float, int]] = None  # number
    wet_bulb_globe_temperature: Optional[Union[float, int]] = None  # number
    air_density: Optional[Union[float, int]] = None  # number
    delta_t: Optional[Union[float, int]] = None  # numberv
    precip_minutes_local_day: Optional[Union[float, int]] = None  # number
    precip_minutes_local_yesterday: Optional[Union[float, int]] = None  # number

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["DeviceObservationSummary"]
