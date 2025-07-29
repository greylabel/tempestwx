"""
Tempest configuration
"""
import os as _os
from dotenv import load_dotenv as _load_env_vars

from tempestwx.version import __version__

_load_env_vars()

TEMPEST_DEBUG = _os.environ.get('TEMPEST_DEBUG', "False").lower() == "true"
TEMPEST_API_URI = _os.environ.get('TEMPEST_API_URI', 'https://swd.weatherflow.com/swd/rest/')
TEMPEST_LOGGER_FORMAT = _os.environ.get('TEMPEST_LOGGER_FORMAT', '%(asctime)s %(levelname)s %(message)s')
TEMPEST_SDK_VERSION = __version__
TEMPEST_USER_AGENT = f'tempest-sdk/python/v{TEMPEST_SDK_VERSION}'

TEMPEST_UNIT_TEMPERATURE = _os.environ.get('TEMPEST_DEFAULT_UNIT_TEMPERATURE', 'c')
TEMPEST_UNIT_PRESSURE = _os.environ.get('TEMPEST_DEFAULT_UNIT_PRESSURE', 'mb')
TEMPEST_UNIT_WIND = _os.environ.get('TEMPEST_DEFAULT_UNIT_WIND', 'mps')
TEMPEST_UNIT_DISTANCE = _os.environ.get('TEMPEST_DEFAULT_UNIT_DISTANCE', 'km')
TEMPEST_UNIT_PRECIP = _os.environ.get('TEMPEST_DEFAULT_UNIT_PRECIP', 'mm')
