"""Curated public model exports.

We intentionally re-export only a focused set of user-facing models &
enums. Internal / lower-level structures remain available from their
respective submodules but are not part of the stable public surface.

Guidelines for inclusion:
  * Used directly by higher-level client API methods, OR
  * Commonly instantiated / inspected by library consumers.

If something you relied upon is no longer exported here, import it from
its concrete module (e.g. ``from tempestwx._models.rapid_wind import
RapidWind``).
Open an issue if you believe an omitted symbol should be public.
"""

from ._serializer import Model
from .better_forecast import BetterForecast
from .station import Station
from .station_observation_latest import StationObservationLatest
from .station_observations import StationObservation
from .station_set import StationSet
from .stats_set import StatsSet
from .status import Status
from .units_default import UnitsDefault

__all__ = [
    # Core base / utilities
    "Model",
    # High-level domain models
    "BetterForecast",
    "Station",
    "StationSet",
    "StationObservation",
    "StationObservationLatest",
    "StatsSet",
    "Status",
    # Common enums / config
    "UnitsDefault",
]

# NOTE: Intentionally NOT exporting internal / finer-grained models such as:
#   * BetterForecast sub-component models
#   * Daily observation variants (Tempest/Air/Sky)
#   * RapidWind, LightningEvent
#   * Device*, StationItem, StationMeta, StationUnits, StatsDayEntry, etc.
# These remain available via their specific submodules if needed.
