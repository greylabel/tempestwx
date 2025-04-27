""" Tempest Client"""

__all__ = ["Tempest", "TempestException"]

from collections import defaultdict
import json
import logging
import re
import warnings

import requests
import urllib.parse
import urllib.request

from twx.exceptions import TempestException

logger = logging.getLogger(__name__)


class Tempest:
    """
    Example usage::

        import twx
    """

    max_retries = 3
    default_retry_codes = (429, 500, 502, 503, 504)

    def __init__(
        self,
        auth=None,
    ):
        """
        Creates a Tempest API client.

        :param auth: An access token (optional)
        """
        self.auth = auth
        self.prefix = "https://api.weatherflow.com/swd/rest/"






    def _q(self, value):
        """Quotes a value for inclusion in a URL."""
        return urllib.parse.quote(f"{value}")

    def _get(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        return self._make_request("GET", url, payload, kwargs)

    def observations_device(self, device_id):
        """ """
        # device_id = self._get_id("device", device_id)
        return self._get("observations/device/" + device_id)

    def observations_station(self, station_id):
        """ """
        # station_id = self._get_id("station", station_id)
        # return self._get("observations/station/" + station_id)

    def stations(self):
        """ """
        return self._get("stations/")

    def stations_station(self, station_id):
        """ """
        # station_id = self._get_id("station", station_id)
        return self._get("stations/" + station_id)

    def better_forcast(self):
        """ """
        return self._get("better_forcast/")
