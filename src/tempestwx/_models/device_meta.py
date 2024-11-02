"""DeviceMeta model with Environment enum."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict

from ._serializer import Model
from .units_default import Environment


class DeviceMeta(Model):
    agl: Optional[Union[float, int]] = None  # float
    name: Optional[str] = None  # string
    environment: Optional[Environment] = None  # string enum
    wifi_network_name: Optional[str] = None  # string

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )


__all__ = ["DeviceMeta"]
