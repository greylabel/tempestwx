"""Rapid Wind (rapid_wind) array model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model

Numeric = Optional[Union[int, float]]
Raw = Union[str, int, float, None]


class RapidWind(Model):
    """Structured representation of a rapid_wind array entry.

    Indices (0..2):
    0: timestamp (s)
    1: wind_speed (m/s)
    2: wind_direction (deg)
    """

    timestamp: Numeric = None
    wind_speed: Numeric = None
    wind_direction: Numeric = None

    @classmethod
    def from_array(cls, array: list[Raw]) -> RapidWind:
        padded = list(array) + [None] * (3 - len(array))
        return cls(  # type: ignore[arg-type]
            timestamp=padded[0],
            wind_speed=padded[1],
            wind_direction=padded[2],
        )

    def to_array(self) -> list[Union[int, float, None]]:
        return [self.timestamp, self.wind_speed, self.wind_direction]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
    )


__all__ = ["RapidWind"]
