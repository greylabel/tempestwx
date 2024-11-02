"""BetterForecast model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .better_forecast_current_conditions import BetterForecastCurrentConditions
from .better_forecast_forecast import BetterForecastForecast
from .better_forecast_units import BetterForecastUnits
from .status import Status


class BetterForecast(Model):
    latitude: Optional[Union[float, int]] = None  # float
    longitude: Optional[Union[float, int]] = None  # float
    timezone: Optional[str] = None  # string
    timezone_offset_minutes: Optional[Union[float, int]] = None  # number
    location_name: Optional[str] = None  # string
    current_conditions: Optional[BetterForecastCurrentConditions] = None  # object
    forecast: Optional[BetterForecastForecast] = None  # object
    status: Optional[Status] = None  # object
    units: Optional[BetterForecastUnits] = None  # object
    source_id_conditions: Optional[Union[float, int]] = None  # number

    # Omitted from docs but present in API
    # station:

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = [
    "BetterForecast",
]
