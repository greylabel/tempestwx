from __future__ import annotations

from tempestwx._client.base import TempestBase
from tempestwx._client.decorators import make_request
from tempestwx._client.processor import model_instance
from tempestwx._models.stats_set import StatsSet


class TempestStats(TempestBase):
    """
    Stats API endpoints.
    """

    @make_request(model_instance(StatsSet))
    def stats(self, station_id: int) -> StatsSet:
        """Get statistics for a specific station.

        Wrapper for Tempest Weather API endpoint:
        https://apidocs.tempestwx.com/reference/get_stats-station-station-id

        Parameters
        ----------
        station_id : int
            Unique station identifier. Must be a positive integer.

        Returns
        -------
        StatsSet
            Aggregated statistics for the station.

        Raises
        ------
        ValueError
            If ``station_id`` is not positive.
        """

        if station_id <= 0:
            raise ValueError("station_id must be a positive integer.")

        return self._get(f"stats/station/{station_id}")
