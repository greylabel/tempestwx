from __future__ import annotations

from collections.abc import Coroutine
from contextvars import ContextVar
from enum import Enum
from typing import TypeVar

from tempestwx._http import Client, Request, Response, Transport
from tempestwx.settings import Settings
from tempestwx.settings_loader import load_settings

# Type variable for generic enum validation (module-scoped)
_E = TypeVar("_E", bound=Enum)


class TempestBase(Client):
    _token_cv: ContextVar[str] = ContextVar("_token_cv")

    def __init__(
        self,
        token: str | None = None,
        transport: Transport | None = None,
        asynchronous: bool | None = None,
        settings: Settings | None = None,
    ) -> None:
        super().__init__(transport, asynchronous)
        base_settings = settings or load_settings()
        self.settings = (
            base_settings.with_overrides(token=token) if token is not None else base_settings
        )
        self._token = self.settings.token

    @property
    def token(self):
        return self._token_cv.get(self._token)

    @token.setter
    def token(self, value: str) -> None:
        try:
            self._token_cv.get()
        except LookupError:
            self._token = value
        else:
            self._token_cv.set(value)

    def __repr__(self) -> str:
        options = [
            f"token={self.token!r}",
            f"transport={self.transport!r}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    def _create_headers(self, content_type: str = "application/json"):
        return {
            "Authorization": f"Bearer {self.token!s}",
            "Content-Type": content_type,
        }

    @staticmethod
    def _validate_enum_param(
        param_name: str,
        value: _E | str | int,
        enum_class: type[_E],
    ) -> _E:
        """
        Validate and convert a parameter to its enum type.

        Parameters
        ----------
        param_name : str
            Name of the parameter (for error messages).
        value : E | str | int
            The value to validate (enum instance or literal such as string or integer).
        enum_class : type[E]
            The enum class to validate against.

        Returns
        -------
        E
            The validated enum instance.

        Raises
        ------
        ValueError
            If the value is not a valid member of the enum.
        """
        if isinstance(value, enum_class):
            return value  # type: ignore[return-value]

        # Attempt to coerce common literal types (e.g., str, int) to the enum
        try:
            return enum_class(value)  # type: ignore[arg-type,return-value]
        except (ValueError, TypeError):
            valid_values = [e.value for e in enum_class]
            raise ValueError(
                "Invalid {p}: {v!r}. Valid: {vals}".format(p=param_name, v=value, vals=valid_values)
            )

    def send(self, request: Request) -> Response | Coroutine[None, None, Response]:
        """
        Build request url and headers, and send with underlying transport.

        Exposed to easily send arbitrary requests,
        for custom behavior in some endpoint e.g. for a subclass.
        It may also come in handy if a bugfix or a feature is not implemented
        in a timely manner, or in debugging related to the client or Web API.
        """
        request.url = self._build_url(request.url)
        headers = self._create_headers()
        if request.headers is not None:
            headers.update(request.headers)
        request.headers = headers
        return self.transport.send(request)

    def _build_url(self, url: str) -> str:
        """Attach API base URL if needed (scheme-agnostic)."""
        if not url.startswith("https"):
            url = self.settings.api_uri_normalized + url.lstrip("/")
        return url

    @staticmethod
    def _parse_url_params(params: dict | None) -> dict | None:
        """Generate parameter dict and filter Nones."""
        params = params or {}
        return {k: v for k, v in params.items() if v is not None} or None

    @staticmethod
    def _request(
        method: str,
        url: str,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> tuple[Request, tuple]:
        return (
            Request(
                method=method,
                url=url,
                params=TempestBase._parse_url_params(params),
                json=payload,
            ),
            (),
        )

    def _get(self, url: str, payload: dict | None = None, **params):
        req, extra = self._request("GET", url, payload=payload, params=params)
        req.url = self._build_url(req.url)
        return req, extra

    def _post(self, url: str, payload: dict | None = None, **params):
        req, extra = self._request("POST", url, payload=payload, params=params)
        req.url = self._build_url(req.url)
        return req, extra

    def _delete(self, url: str, payload: dict | None = None, **params):
        req, extra = self._request("DELETE", url, payload=payload, params=params)
        req.url = self._build_url(req.url)
        return req, extra

    def _put(self, url: str, payload: dict | None = None, **params):
        req, extra = self._request("PUT", url, payload=payload, params=params)
        req.url = self._build_url(req.url)
        return req, extra
