# Tempest

Python client for the Tempest Weather API.

## Features

- Typed Pydantic v2 models for core API responses
- Composable client mixins for forecast, stations, observations, stats
- Config cascade (defaults → JSON → .env → environment → explicit overrides)
- Immutable settings object with easy override layering
- Optional automatic `.env` loading when `python-dotenv` is installed
- Convenience `reload_settings()` for dynamic environments (tests / REPL)
- Sync and async usage via a single client (`asynchronous=True`)

## Installation

Requires Python 3.13+.

- From PyPI (when available):

  pip install tempestwx

- From Git (latest main):

  pip install git+<https://github.com/greylabel/tempestwx.git>

## Usage

```python
from tempestwx import Tempest

twx = Tempest()  # Token resolved via .env or environment
stations = twx.stations()
print(stations)
```

### Configuration & Settings

The client uses a deterministic cascade to resolve configuration:

1. Library defaults (built‑in constants)
2. `config.json` (first existing among: `$TEMPEST_CONFIG_PATH`, `./config.json`)
3. `.env` file (loaded automatically once, without overriding already exported environment vars)
4. Live environment variables (take precedence over `.env` values)
5. Explicit parameters passed to `Tempest(...)` (highest precedence)

Resolved values are materialized into an immutable `Settings` instance:

```python
from tempestwx.settings_loader import load_settings
settings = load_settings()
print(settings.api_uri, settings.token)
```

You can explicitly override when constructing the client:

```python
from tempestwx import Tempest
twx = Tempest(token="OVERRIDE_TOKEN")
```

Or derive a modified settings object:

```python
from tempestwx.settings_loader import load_settings
base = load_settings()
custom = base.with_overrides(api_uri="https://example.test/api/")
twx = Tempest(settings=custom)
```

### Environment Variables

Supported variables:

- `TEMPEST_ACCESS_TOKEN` – API auth token
- `TEMPEST_API_URI` – Base API URI (defaults to `https://swd.weatherflow.com/swd/rest/`)
- `TEMPEST_CONFIG_PATH` – Optional path to a JSON config file (fallbacks to `./config.json`)
- Unit overrides (optional):
  - `TEMPEST_DEFAULT_UNIT_TEMPERATURE`
  - `TEMPEST_DEFAULT_UNIT_PRESSURE`
  - `TEMPEST_DEFAULT_UNIT_WIND`
  - `TEMPEST_DEFAULT_UNIT_DISTANCE`
  - `TEMPEST_DEFAULT_UNIT_PRECIP`
  - `TEMPEST_DEFAULT_UNIT_BRIGHTNESS`
  - `TEMPEST_DEFAULT_UNIT_SOLAR_RADIATION`
  - `TEMPEST_DEFAULT_UNIT_BUCKET_STEP_MINUTES`

### .env Support

If a `.env` file exists in the working directory, it is loaded automatically (without overriding already exported variables) the first time `load_settings()` runs.

Example `.env`:

```dotenv
TEMPEST_ACCESS_TOKEN=your-token-here
```

### Reloading Settings

Caching avoids repeated disk & env parsing. To pick up changes at runtime:

```python
from tempestwx.settings_loader import reload_settings
reload_settings()  # clears cache and re-evaluates cascade
```

### Units Overrides

You can supply partial unit overrides via `UnitsOverrides` (only fields you specify are changed):

```python
from tempestwx.settings import UnitsOverrides
from tempestwx.settings_loader import load_settings

base = load_settings()
custom = base.with_overrides(units_overrides=UnitsOverrides(temp="f", wind="mph"))
twx = Tempest(settings=custom)
```

### Token Context Override

Temporarily swap tokens:

```python
from tempestwx import Tempest

twx = Tempest()
with twx.token_as("temporary-token"):
    stations = twx.stations()
```

### Error Handling

HTTP errors raise subclasses of `HTTPError` (e.g. `NotFound`, `TooManyRequests`). You can extend transports for retry/caching behavior by composing custom transport implementations.

Example:

```python
from tempestwx import Tempest
from tempestwx._http.error import NotFound, TooManyRequests

twx = Tempest()
try:
    latest = twx.obs_station_latest(station_id=123)
except NotFound:
    print("Station not found")
except TooManyRequests:
    print("Rate limit exceeded; retry later")
```

### Async Usage

All endpoints support async when the client is created with `asynchronous=True`:

```python
import asyncio
from tempestwx import Tempest

async def main():
    twx = Tempest(asynchronous=True)
    stations = await twx.stations()
    print(stations)

asyncio.run(main())
```

### Endpoint quick reference

All methods return typed Pydantic models. Below are the most-used calls with their return types.

- Stations
  - `stations() -> StationSet`
  - `station(station_id: int) -> StationSet`

- Observations
  - `obs_station(station_id: int, start_time=None, end_time=None, bucket=1, obs_fields="", units_...) -> StationObservation`
  - `obs_device(device_id: int, day_offset=0, time_start=None, time_end=None, format=None) -> DeviceObservation`
  - `obs_station_latest(station_id: int) -> StationObservationLatest`

- Better Forecast
  - `forecast(station_id: int, units_...) -> BetterForecast`

- Stats
  - `stats(station_id: int) -> StatsSet`

Quick examples (sync):

```python
from tempestwx import Tempest

twx = Tempest()
stations = twx.stations()  # StationSet
one = twx.station(123)  # StationSet
obs = twx.obs_station(123, start_time=0, end_time=0)  # StationObservation
device_obs = twx.obs_device(456, day_offset=1)  # DeviceObservation
latest = twx.obs_station_latest(123)  # StationObservationLatest
forecast = twx.forecast(123, units_temp="f")  # BetterForecast
stats = twx.stats(123)  # StatsSet
```

Async equivalents:

```python
from tempestwx import Tempest

twx = Tempest(asynchronous=True)
stations = await twx.stations()
latest = await twx.obs_station_latest(123)
```

### config.json example

If present, values provide defaults that can be overridden by environment variables:

```json
{
  "api_uri": "https://swd.weatherflow.com/swd/rest/",
  "default_unit_temperature": "c",
  "default_unit_pressure": "mb",
  "default_unit_wind": "mps",
  "default_unit_distance": "km",
  "default_units_precip": "mm",
  "default_units_brightness": "lux",
  "default_units_solar_radiation": "w/m2",
  "default_units_bucket_step_minutes": 1
}
```

Note: tokens are not read from `config.json`. Use environment variables or `.env` for `TEMPEST_ACCESS_TOKEN`.

## Caveats

- Ensure `TEMPEST_ACCESS_TOKEN` is set (via environment or `.env`) before making calls.
- The client returns Pydantic models. Use `.model_dump()` to convert to `dict` when needed.

## Troubleshooting

- “Unauthorized” or 401 errors: verify `TEMPEST_ACCESS_TOKEN`.
- Wrong base URL: confirm `TEMPEST_API_URI` (Settings normalizes it to end with a slash).
- Unit overrides not taking effect: ensure you’re using the correct env var names listed above. If using `.env`, call `reload_settings()` after editing.

## Reporting Issues

## Contributing
