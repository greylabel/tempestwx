"""StationMeta model."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model


class StationMeta(Model):
    elevation: Optional[Union[float, int]] = None  # float
    share_with_wf: Optional[bool] = True  # boolean
    share_with_wu: Optional[bool] = True  # boolean

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        strict=True,
    )


__all__ = ["StationMeta"]
