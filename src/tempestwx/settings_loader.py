"""Settings cascade loader.

Resolves configuration in the following precedence order (highest last):
    1. Library defaults (code)
    2. JSON config file (if present)
    3. ``.env`` and live environment variables (``.env`` loaded non-overriding)
    4. Explicit overrides provided by caller (applied outside this module)

This module exposes :func:`load_settings` which returns a cached
(:func:`functools.lru_cache`) :class:`~tempestwx.settings.Settings`
instance. Callers can derive variants via
:meth:`tempestwx.settings.Settings.with_overrides`.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv as _load_dotenv

from ._models.units_default import UnitsDefault
from .settings import Settings, UnitsOverrides

# Candidate config file paths to scan (first existing wins)
_CONFIG_CANDIDATES = [
    # Explicit path via env var
    os.environ.get("TEMPEST_CONFIG_PATH"),
    # Project local
    str(Path.cwd() / "config.json"),
]

_JSON_KEY_MAP = {
    "api_uri": "api_uri",
    # Units
    "default_unit_temperature": "units_temp",
    "default_unit_pressure": "units_pressure",
    "default_unit_wind": "units_wind",
    "default_unit_distance": "units_distance",
    "default_units_precip": "units_precip",
    "default_units_brightness": "units_brightness",
    "default_units_solar_radiation": "units_solar_radiation",
    "default_units_bucket_step_minutes": "bucket",
}

_ENV_UNIT_MAP = {
    "TEMPEST_DEFAULT_UNIT_TEMPERATURE": "units_temp",
    "TEMPEST_DEFAULT_UNIT_PRESSURE": "units_pressure",
    "TEMPEST_DEFAULT_UNIT_WIND": "units_wind",
    "TEMPEST_DEFAULT_UNIT_DISTANCE": "units_distance",
    "TEMPEST_DEFAULT_UNIT_PRECIP": "units_precip",
    "TEMPEST_DEFAULT_UNIT_BRIGHTNESS": "units_brightness",
    "TEMPEST_DEFAULT_UNIT_SOLAR_RADIATION": "units_solar_radiation",
    "TEMPEST_DEFAULT_UNIT_BUCKET_STEP_MINUTES": "bucket",
}


def _first_existing_path() -> Path | None:
    for candidate in _CONFIG_CANDIDATES:
        if candidate:
            p = Path(candidate)
            if p.is_file():
                return p
    return None


def _load_json(path: Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _build_units(default: UnitsDefault, json_cfg: Dict[str, Any]) -> UnitsDefault:
    # Start with defaults and overlay JSON + env
    updates: Dict[str, Any] = {}
    # JSON first
    for json_key, attr in _JSON_KEY_MAP.items():
        if (
            json_key.startswith("default_unit") or json_key.startswith("default_units")
        ) and json_key in json_cfg:
            updates[attr] = json_cfg[json_key]
    # Env overrides
    for env_key, attr in _ENV_UNIT_MAP.items():
        val = os.environ.get(env_key)
        if val is not None:
            updates[attr] = val
    if not updates:
        return default
    # Normalize bucket (int) else leave textual enums
    bucket_val = updates.get("bucket")
    if bucket_val is not None:
        try:
            updates["bucket"] = int(bucket_val)
        except ValueError:
            updates.pop("bucket", None)
    return default.model_copy(update=updates)


@lru_cache
def load_settings() -> Settings:
    """Load and cache Settings from defaults, JSON, and environment.

    The ``.env`` file (if present) is loaded once on first call with
    ``override=False`` to preserve already-exported environment variables.
    """
    # Ensure .env is considered early (only once due to caching)
    if _load_dotenv is not None:
        # Respect real environment variables over .env by default
        _load_dotenv(".env", override=False)
    json_cfg = _load_json(_first_existing_path())
    base = Settings()
    units = _build_units(base.units, json_cfg)
    api_uri = os.environ.get("TEMPEST_API_URI") or json_cfg.get("api_uri") or base.api_uri
    token = os.environ.get("TEMPEST_ACCESS_TOKEN") or None
    return Settings(api_uri=api_uri, token=token, units=units)


def reload_settings() -> Settings:
    """Clear cached settings and reload (useful after env mutation).

    On reload, refresh ``.env`` values with ``override=True`` so changes in
    the file are applied even if a prior call populated ``os.environ``. This
    does not impact callers who explicitly set environment variables within
    the same process after this call.
    """
    load_settings.cache_clear()  # type: ignore[attr-defined]
    if _load_dotenv is not None:
        _load_dotenv(".env", override=True)
    return load_settings()


__all__ = ["load_settings", "reload_settings", "UnitsOverrides"]
