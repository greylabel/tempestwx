"""Lightning event (evt_strike) array model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model

Numeric = Optional[Union[int, float]]
Raw = Union[str, int, float, None]


class LightningEvent(Model):
    """Structured representation of an evt_strike array entry.

    Indices (0..2):
    0: timestamp (s)
    1: distance (km)
    2: energy
    """

    timestamp: Numeric = None
    distance: Numeric = None
    energy: Numeric = None

    @classmethod
    def from_array(cls, array: list[Raw]) -> LightningEvent:
        padded = list(array) + [None] * (3 - len(array))
        return cls(  # type: ignore[arg-type]
            timestamp=padded[0],
            distance=padded[1],
            energy=padded[2],
        )

    def to_array(self) -> list[Union[int, float, None]]:
        return [self.timestamp, self.distance, self.energy]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
    )


__all__ = ["LightningEvent"]
