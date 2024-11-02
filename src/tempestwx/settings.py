"""Configuration settings and overrides for the Tempest client.

This module defines a structured, immutable configuration object used by
the client to avoid reliance on scattered globals. Resolution of values
from files and environment is handled externally (see
``settings_loader.py``).

Effective precedence (highest last, applied during load):
    explicit overrides > environment variables (incl. values loaded from
    a ``.env`` file by the loader) > JSON config > library defaults.

The goal is to keep :class:`Settings` immutable so that a single
instance can be safely shared across threads and async contexts.
"""

from __future__ import annotations

from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field

from ._models.units_default import (
    Bucket,
    UnitsBrightness,
    UnitsDefault,
    UnitsDistance,
    UnitsPrecip,
    UnitsPressure,
    UnitsSolarRadiation,
    UnitsTemp,
    UnitsWind,
)

_DEFAULT_API_URI = "https://swd.weatherflow.com/swd/rest/"


class UnitsOverrides(BaseModel):
    """Partial override fields for units.

    Only supply the fields you want to change relative to the base
    UnitsDefault. The `apply` method returns a new UnitsDefault instance
    with modifications.
    """

    temp: Optional[UnitsTemp] = None
    wind: Optional[UnitsWind] = None
    pressure: Optional[UnitsPressure] = None
    precip: Optional[UnitsPrecip] = None
    distance: Optional[UnitsDistance] = None
    brightness: Optional[UnitsBrightness] = None
    solar_radiation: Optional[UnitsSolarRadiation] = None
    bucket: Optional[Bucket] = None

    def apply(self, base: UnitsDefault) -> UnitsDefault:
        """Return a new UnitsDefault with these overrides applied.

        Only fields set on this overrides object are changed; all others
        inherit from the provided ``base``.
        """
        return UnitsDefault(
            units_temp=self.temp or base.units_temp,
            units_pressure=self.pressure or base.units_pressure,
            units_wind=self.wind or base.units_wind,
            units_distance=self.distance or base.units_distance,
            units_brightness=self.brightness or base.units_brightness,
            units_solar_radiation=(self.solar_radiation or base.units_solar_radiation),
            units_precip=self.precip or base.units_precip,
            bucket=self.bucket or base.bucket,
        )


class Settings(BaseModel):
    """Immutable configuration for a Tempest client instance."""

    api_uri: str = Field(default=_DEFAULT_API_URI)
    token: Optional[str] = None
    units: UnitsDefault = Field(default_factory=UnitsDefault)

    model_config = {
        "frozen": True,
        "extra": "ignore",
        "str_strip_whitespace": True,
    }

    def with_overrides(
        self,
        *,
        token: str | None = None,
        api_uri: str | None = None,
        units: UnitsDefault | None = None,
        units_overrides: UnitsOverrides | None = None,
    ) -> "Settings":
        """Return a new Settings with selected fields overridden.

        Parameters
        ----------
        token : str | None
            If provided, overrides the current token. If omitted, the
            existing token is preserved.
        api_uri : str | None
            If provided, overrides the current API base URI. If omitted,
            the existing URI is preserved.
        units : UnitsDefault | None
            If provided, replaces the current units entirely.
        units_overrides : UnitsOverrides | None
            If provided (and ``units`` is not), applies only those unit
            fields set on the overrides object.

        Returns
        -------
        Settings
            A new immutable Settings instance reflecting the requested
            changes.
        """
        new_units = units or (units_overrides.apply(self.units) if units_overrides else self.units)
        return Settings(
            api_uri=api_uri or self.api_uri,
            token=self.token if token is None else token,
            units=new_units,
        )

    @cached_property
    def api_uri_normalized(self) -> str:
        """Return the API base URI guaranteed to end with a single slash."""
        return self.api_uri.rstrip("/") + "/"


__all__ = ["Settings", "UnitsOverrides"]
