from __future__ import annotations

from tempestwx._client.base import TempestBase
from tempestwx._client.decorators import make_request
from tempestwx._client.processor import model_instance
from tempestwx._models.station_set import StationSet


class TempestStations(TempestBase):
    """
    Stations API endpoints.
    """

    @make_request(model_instance(StationSet))
    def stations(self) -> StationSet:
        """List all stations associated with the authenticated account.

        Wrapper for Tempest Weather API endpoint:
        https://apidocs.tempestwx.com/reference/get_stations

        Returns
        -------
        StationSet
            Collection of station metadata.
        """
        return self._get("stations")

    @make_request(model_instance(StationSet))
    def station(self, station_id: int) -> StationSet:
        """Get metadata/details for a specific station.

        Wrapper for Tempest Weather API endpoint:
        https://apidocs.tempestwx.com/reference/getstationbyid

        Parameters
        ----------
        station_id : int
            Unique station identifier. Must be a positive integer.

        Returns
        -------
        StationSet
            Station metadata container (single station entry).

        Raises
        ------
        ValueError
            If ``station_id`` is not positive.
        """

        if station_id <= 0:
            raise ValueError("station_id must be a positive integer.")

        return self._get(f"stations/{station_id}")
