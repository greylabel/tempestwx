"""Tempest Personal Access Token (PAT) authentication.
This module provides a class for handling authentication with the Tempest API using a personal access token (PAT).
"""

__all__ = ["TempestPersonalAccessToken"]

import logging
import os
from typing import Dict

from dotenv import load_dotenv

from tempestwx.exceptions import TempestException

load_dotenv("./.env", override=True)
logger = logging.getLogger(__name__)

PAT_CRED_ENV_VARS: dict = {
    "personal_access_token": "TEMPEST_PERSONAL_ACCESS_TOKEN",
}

def _ensure_value(value, env_key):
    env_val = PAT_CRED_ENV_VARS[env_key]
    _val = value or os.getenv(env_val)
    if _val is None:
        msg = f"No {env_key}. Pass it or set a {env_val} environment variable."
        raise TempestException(msg)
    return _val


class TempestPersonalAccessToken:
    """
    Tempest Personal Access Token (PAT) authentication.
    This class is used to authenticate with the Tempest API using a personal access token.
    """

    def __init__(self, personal_access_token=None) -> None:
        self.personal_access_token = personal_access_token

    @property
    def personal_access_token(self) -> str | None:
        """Get the personal access token."""
        return self._personal_access_token

    @personal_access_token.setter
    def personal_access_token(self, value: str) -> None:
        """Set the personal access token."""
        self._personal_access_token = _ensure_value(value, "personal_access_token")

    def get_auth_header(self) -> Dict[str, str]:
        """Get the authorization header for the personal access token."""
        return {"Authorization": f"Bearer {self.personal_access_token}"}
