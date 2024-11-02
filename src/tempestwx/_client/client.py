from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from tempestwx._http import Transport
from tempestwx.settings import Settings
from tempestwx.settings_loader import load_settings

from .api import (
    TempestBetterForecast,
    TempestObservations,
    TempestStations,
    TempestStats,
)


class Tempest(
    TempestBetterForecast,
    TempestObservations,
    TempestStations,
    TempestStats,
):
    """
    Tempest API client.
    """

    def __init__(
        self,
        token: str | None = None,
        transport: Transport | None = None,
        asynchronous: bool | None = None,
        settings: Settings | None = None,
    ) -> None:
        """
        Initialize Tempest client.

        Parameters
        ----------
        token : str | None, optional
            Access token. If not provided, falls back to
            `settings.token` or the value resolved by `load_settings()` which
            reads TEMPEST_ACCESS_TOKEN from the environment (with .env support
            when python-dotenv is installed).
        transport : Transport | None, optional
            Custom HTTP transport implementation.
        asynchronous : bool | None, optional
            Whether to use async/await pattern.
        settings : Settings | None, optional
            Preconstructed settings to use (overrides API URI/units/token
            resolution via `load_settings()` if provided). Note: token in
            settings typically comes from TEMPEST_ACCESS_TOKEN; config.json does
            not store tokens.
        """

        if token is None:
            base_settings = settings or load_settings()
            resolved_token = base_settings.token
            settings = base_settings
        else:
            resolved_token = token
        super().__init__(
            token=resolved_token,
            transport=transport,
            asynchronous=asynchronous,
            settings=settings,
        )

    @contextmanager
    def token_as(self, token: str) -> Generator["Tempest", None, None]:
        """
        Temporarily override the access token within a context.

        Parameters
        ----------
        token : str
            Temporary access token to use for API calls within this context.

        Yields
        ------
        Tempest
            This client instance with the overridden token.

        Examples
        --------
        >>> client = Tempest()  # Uses TEMPEST_ACCESS_TOKEN from env
        >>> with client.token_as("temporary_token"):
        ...     stations = client.get_stations()  # Uses temporary_token
        >>> # Back to original token
        """
        cv_token = self._token_cv.set(token)
        try:
            yield self
        finally:
            self._token_cv.reset(cv_token)
