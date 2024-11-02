"""Status model"""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict, field_validator

from ._serializer import Model


class Status(Model):
    status_code: Optional[int] = None  # int32
    status_message: Optional[str] = None  # string

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        str_strip_whitespace=True,
        strict=True,
    )

    @field_validator("status_message")
    @classmethod
    def _empty_str_to_none(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() == "":
            return None
        return v


__all__ = ["Status"]
