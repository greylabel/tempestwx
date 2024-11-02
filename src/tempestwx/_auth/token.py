from __future__ import annotations

from abc import ABC, abstractmethod


class AccessToken(ABC):
    """Access Token base class."""

    @property
    @abstractmethod
    def access_token(self) -> str:
        """
        Bearer token.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Return the string representation of the Bearer token.
        """
        return self.access_token


class Token(AccessToken):
    """
    Access Token implementation.

    Represents a Personal Access Tokens (PAT).
    OAuth Authorization Code (with PKCE) grant types are not yet supported.
    """

    def __init__(self, token_details: dict) -> None:
        self._access_token = token_details["access_token"]

    def __repr__(self) -> str:
        options = [
            f"access_token={self.access_token!r}",
        ]
        return type(self).__name__ + "(" + ", ".join(options) + ")"

    @property
    def access_token(self) -> str:
        """Bearer token."""
        return self._access_token
