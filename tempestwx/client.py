"""Tempest Client"""

__all__ = ["Tempest", "TempestException"]

import json
import logging
import re
import time
from collections import defaultdict

import requests

from tempestwx import config
from tempestwx.exceptions import TempestException

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Tempest:
    """
    Example usage::

        import tempestwx as twx
    """

    max_retries = 3
    default_retry_codes = (429, 500, 502, 503, 504)
    _regex_unit_temp = r"^(c|f)$"
    _regex_unit_wind = r"^(mph|kph|kts|mps|bft|lfm)$"
    _regex_unit_pressure = r"^(mb|inhg|mmhg|hpa)$"
    _regex_unit_precip = r"^(mm|cm|in)$"
    _regex_unit_distance = r"^(km|mi)$"
    _regex_bucket_time_resolutions = r"^(1|5|30|180)$"
    _regex_reponse_format = r"^(csv)$"

    def __init__(
        self,
        auth=None,
        # requests_session=True,
        # client_credentials_manager=None,
        # oauth_manager=None,
        auth_manager=None,
        proxies=None,
        requests_timeout=5,
        status_forcelist=None,
        retries=max_retries,
        status_retries=max_retries,
        backoff_factor=0.3,
    ):
        """
        Creates a Tempest API client.

        :param auth: An access token (optional)
        :param auth_manager:
            TempestPersonalAccessToken instance (optional)
        """
        self.prefix: str = config.TEMPEST_API_URI
        self._auth = auth
        # self.client_credentials_manager = client_credentials_manager
        # self.oauth_manager = oauth_manager
        self.auth_manager = auth_manager
        self.proxies = proxies
        self.requests_timeout = requests_timeout
        self.status_forcelist = status_forcelist or self.default_retry_codes
        self.backoff_factor = backoff_factor
        self.retries = retries
        self.status_retries = status_retries

        # Use the Requests API module as a "session".
        self._session = requests.api

    def set_auth(self, auth):
        self._auth = auth

    @property
    def auth_manager(self):
        return self._auth_manager

    @auth_manager.setter
    def auth_manager(self, auth_manager):
        if auth_manager is not None:
            self._auth_manager = auth_manager

    def _auth_headers(self):
        if self._auth:
            return {"Authorization": f"Bearer {self._auth}"}
        if not self.auth_manager:
            return {}
        try:
            token = self.auth_manager.get_access_token(as_dict=False)
        except TypeError:
            token = self.auth_manager.get_access_token()
        return {"Authorization": f"Bearer {token}"}

    def _internal_call(self, method, url, payload, params):
        args = dict(params=params)
        if not url.startswith("https"):
            url = self.prefix + url
        headers = self._auth_headers()

        if "content_type" in args["params"]:
            headers["Content-Type"] = args["params"]["content_type"]
            del args["params"]["content_type"]
            if payload:
                args["data"] = payload
        else:
            headers["Content-Type"] = "application/json"
            if payload:
                args["data"] = json.dumps(payload)

        logger.debug(
            f"Sending {method} to {url} with Params: "
            f"{args.get('params')} Headers: {headers} and Body: {args.get('data')!r}"
        )

        try:
            response = self._session.request(
                method,
                url,
                headers=headers,
                proxies=self.proxies,
                timeout=self.requests_timeout,
                **args,
            )

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            try:
                json_response = response.json()
                error = json_response.get("error", {})
                msg = error.get("message")
                reason = error.get("reason")
            except ValueError:
                # if the response cannot be decoded into JSON (which raises a ValueError),
                # then try to decode it into text

                # if we receive an empty string (which is falsy), then replace it with `None`
                msg = response.text or None
                reason = None

            logger.error(
                f"HTTP Error for {method} to {url} with Params: "
                f"{args.get('params')} returned {response.status_code} due to {msg}"
            )

            raise TempestException(
                response.status_code,
                -1,
                f"{response.url}:\n {msg}",
                reason=reason,
                headers=response.headers,
            )
        except requests.exceptions.RetryError as retry_error:
            request = retry_error.request
            logger.error("Max Retries reached")
            try:
                reason = retry_error.args[0].reason
            except (IndexError, AttributeError):
                reason = None
            raise TempestException(
                429, -1, f"{request.path_url}:\n Max Retries", reason=reason
            )
        except ValueError:
            results = None

        logger.debug(f"RESULTS: {results}")
        return results

    def _get(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call("GET", url, payload, kwargs)

    def station(self, station_id: int):
        """Get metadata for a specific station owned by the user.
        :param station_id: The station ID
        :type station_id: int
        """
        sid = self._get_id(station_id)
        return self._get("stations/" + str(sid))

    def stations(self):
        """Get the metadata for all stations you have access to."""
        return self._get("stations/")

    def obs_station(
        self,
        station_id: int,
        time_start: int | None = None,
        time_end: int | None = None,
        bucket: int = 1,
        obs_fields: str | None = None,
        units_temp: str | None = config.TEMPEST_UNIT_TEMPERATURE,
        units_wind: str = config.TEMPEST_UNIT_WIND,
        units_pressure: str = config.TEMPEST_UNIT_PRESSURE,
        units_precip: str = config.TEMPEST_UNIT_PRECIP,
        units_distance: str = config.TEMPEST_UNIT_DISTANCE,
    ):
        """Get observations for a station."""
        sid = self._get_id(station_id)
        t_start = self._get_timestamp(time_start) if time_start else None
        t_end = self._get_timestamp(time_end) if time_end else None
        bucket_res = self._get_bucket_time_resolution(bucket)
        temp_unit = self._get_temp_unit(units_temp)
        wind_unit = self._get_wind_unit(units_wind)
        pressure_unit = self._get_pressure_unit(units_pressure)
        precip_unit = self._get_precip_unit(units_precip)
        distance_unit = self._get_distance_unit(units_distance)
        return self._get(
            "observations/stn/" + str(sid),
            time_start=t_start,
            time_end=t_end,
            bucket=bucket_res,
            obs_fields=obs_fields,
            units_temp=temp_unit,
            units_wind=wind_unit,
            units_pressure=pressure_unit,
            units_precip=precip_unit,
            units_distance=distance_unit,
        )

    def obs_device(
        self,
        device_id: int,
        day_offset: int | None = None,
        time_start: int | None = None,
        time_end: int | None = None,
        format: str | None = None,
    ):
        """Get observations for a device (Air, Sky, or Tempest)."""
        did = self._get_id(device_id)
        offset = self._get_positive_integer(day_offset) if day_offset else None
        t_start = self._get_timestamp(time_start) if time_start else None
        t_end = self._get_timestamp(time_end) if time_end else None
        fmt = self._get_format(format) if format else None
        return self._get(
            "observations/device/" + str(did),
            day_offset=offset,
            time_start=t_start,
            time_end=t_end,
            format=fmt,
        )

    def obs_station_latest(self, station_id: int):
        """Get the latest observations for a station."""
        sid = self._get_id(station_id)
        return self._get("observations/stn/" + str(sid))

    def stats_station(self, station_id: int):
        """Get a summary of observation data and Statistics for a station.
        :param station_id: The station ID
        :type station_id: int
        """
        sid = self._get_id(station_id)
        return self._get("stats/station/" + str(sid))

    def better_forcast(
        self,
        station_id: int,
        units_temp: str | None = config.TEMPEST_UNIT_TEMPERATURE,
        units_wind: str = config.TEMPEST_UNIT_WIND,
        units_pressure: str = config.TEMPEST_UNIT_PRESSURE,
        units_precip: str = config.TEMPEST_UNIT_PRECIP,
        units_distance: str = config.TEMPEST_UNIT_DISTANCE,
    ):
        """Get current conditions and forecast data for your station."""
        sid = self._get_id(station_id)
        temp_unit = self._get_temp_unit(units_temp)
        wind_unit = self._get_wind_unit(units_wind)
        pressure_unit = self._get_pressure_unit(units_pressure)
        precip_unit = self._get_precip_unit(units_precip)
        distance_unit = self._get_distance_unit(units_distance)
        return self._get(
            "better_forecast/",
            station_id=sid,
            units_temp=temp_unit,
            units_wind=wind_unit,
            units_pressure=pressure_unit,
            units_precip=precip_unit,
            units_distance=distance_unit,
        )

    def _get_id(self, id: int | str) -> int:
        """
        :param id: The station or device ID
        :type id: str
        :return: The station or device ID
        :rtype: int
        """
        try:
            return int(id)
        except ValueError:
            raise TempestException(400, -1, f"Invalid ID: {id}. Must be an integer.")

    def _get_positive_integer(self, value: int) -> int:
        """
        Ensures the input is a valid positive integer and returns it.

        :param value: The value to validate (can be int or str)
        :type value: int or str
        :return: The validated positive integer
        :rtype: int
        :raises ValueError: If the value is not a valid positive integer
        """
        try:
            value = int(value)
            if value <= 0:
                raise ValueError(f"Invalid value: {value}. Must be a positive integer.")
            return value
        except (ValueError, TypeError):
            raise TempestException(
                400, -1, f"Invalid value: {value}. Must be a positive integer."
            )

    def _get_timestamp(self, timestamp: int) -> int:
        """
        Validates that the given timestamp is a valid epoch seconds timestamp.

        :param timestamp: The timestamp to validate
        :type timestamp: int
        :return: The validated timestamp
        :rtype: int
        :raises ValueError: If the timestamp is not a valid epoch seconds timestamp
        """
        try:
            timestamp = int(timestamp)
            # Check if the timestamp can be converted to a valid time
            time.gmtime(timestamp)
            return timestamp
        except ValueError:
            raise TempestException(
                400, -1, f"Invalid timestamp: {timestamp}. Must be an integer."
            )

    def _get_bucket_time_resolution(self, bucket: int) -> int:
        """
        :param bucket: The bucket
        :type bucket: int
        :return: The bucket
        :rtype: int
        """
        if not re.match(self._regex_bucket_time_resolutions, str(bucket)):
            raise TempestException(
                400,
                -1,
                f"Invalid bucket: {bucket}. Must be 1, 5, 30 or 180.",
            )
        return bucket

    def _get_format(self, format: str) -> str:
        """
        :param format: The format
        :type format: str
        :return: The format
        :rtype: str
        """
        if not re.match(self._regex_reponse_format, format):
            raise TempestException(400, -1, f"Invalid format: {format}. Must be 'csv'.")
        return format

    def _get_temp_unit(self, unit) -> str:
        """
        :param unit: The temperature unit
        :type unit: str
        :return: The temperature unit
        :rtype: str
        """
        if not re.match(self._regex_unit_temp, unit):
            raise TempestException(
                400, -1, f"Invalid temperature unit: {unit}. Must be 'c' or 'f'."
            )
        return unit

    def _get_wind_unit(self, unit) -> str:
        """
        :param unit: The wind unit
        :type unit: str
        :return: The wind unit
        :rtype: str
        """
        if not re.match(self._regex_unit_wind, unit):
            raise TempestException(
                400,
                -1,
                f"Invalid wind unit: {unit}. Must be 'mph', 'kph', 'kts', 'mps', 'bft' or 'lfm'.",
            )
        return unit

    def _get_pressure_unit(self, unit) -> str:
        """
        :param unit: The pressure unit
        :type unit: str
        :return: The pressure unit
        :rtype: str
        """
        if not re.match(self._regex_unit_pressure, unit):
            raise TempestException(
                400,
                -1,
                f"Invalid pressure unit: {unit}. Must be 'mb', 'inhg', 'mmhg' or 'hpa'.",
            )
        return unit

    def _get_precip_unit(self, unit) -> str:
        """
        :param unit: The precipitation unit
        :type unit: str
        :return: The precipitation unit
        :rtype: str
        """
        if not re.match(self._regex_unit_precip, unit):
            raise TempestException(
                400,
                -1,
                f"Invalid precipitation unit: {unit}. Must be 'mm', 'cm' or 'in'.",
            )
        return unit

    def _get_distance_unit(self, unit) -> str:
        """
        :param unit: The distance unit
        :type unit: str
        :return: The distance unit
        :rtype: str
        """
        if not re.match(self._regex_unit_distance, unit):
            raise TempestException(
                400, -1, f"Invalid distance unit: {unit}. Must be 'km' or 'mi'."
            )
        return unit
