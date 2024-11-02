"""Lightweight processors used by the client layer.

This module provides small, composable helpers for shaping API response data:

- `pass_through`: returns a value unchanged (useful as a default processor).
- `model_instance`: factory that builds a callable to convert a mapping into
    an instance of a provided `Model` subclass, returning `None` for `None`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeVar

from tempestwx._models import Model

T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=Model)


def pass_through(value: T) -> T:
    return value


def model_instance(
    type_: type[ModelT],
) -> Callable[[Mapping[str, Any] | None], ModelT | None]:
    return lambda data: type_(**data) if data is not None else None
