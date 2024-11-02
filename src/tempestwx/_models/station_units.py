"""StationUnits model."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict

from ._serializer import Model
from .units_default import (
    UnitsAirDensity,
    UnitsBrightness,
    UnitsDirection,
    UnitsDistance,
    UnitsOther,
    UnitsPrecip,
    UnitsPressure,
    UnitsSolarRadiation,
    UnitsTemp,
    UnitsWind,
)


class StationUnits(Model):
    units_temp: Optional[UnitsTemp] = None  # string
    units_wind: Optional[UnitsWind] = None  # string
    units_precip: Optional[UnitsPrecip] = None  # string
    units_pressure: Optional[UnitsPressure] = None  # string
    units_distance: Optional[UnitsDistance] = None  # string
    units_direction: Optional[UnitsDirection] = None  # string
    units_other: Optional[UnitsOther] = None  # string
    units_brightness: Optional[UnitsBrightness] = None  # string
    units_solar_radiation: Optional[UnitsSolarRadiation] = None  # string
    units_air_density: Optional[UnitsAirDensity] = None  # string

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["StationUnits"]
