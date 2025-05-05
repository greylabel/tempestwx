__all__ = ["TempestPersonalAccessToken"]

from dotenv import load_dotenv
import logging
import os
from typing import Any, Dict

from tempestwx.exceptions import TempestException

load_dotenv("./.env", override=True)
logger = logging.getLogger(__name__)

PAT_CRED_ENV_VARS: dict = {
    "personal_access_token": "TEMPEST_PERSONAL_ACCESS_TOKEN",
}

def _make_auth_header(access_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}

def _ensure_value(value, env_key):
    env_val = PAT_CRED_ENV_VARS[env_key]
    _val = value or os.getenv(env_val)
    if _val is None:
        msg = f"No {env_key}. Pass it or set a {env_val} environment variable."
        raise TempestException(msg)
    return _val

class TempestPersonalAccessToken():
    def __init__(self, personal_access_token=None) -> None:
        self.personal_access_token = personal_access_token

    @property
    def personal_access_token(self):
        return self._personal_access_token

    @personal_access_token.setter
    def personal_access_token(self, val):
        self._personal_access_token = _ensure_value(val, "personal_access_token")

    def get_access_token(self) -> str:
        return self.personal_access_token

    def get_auth_header(self) -> Dict[str, str]:
        return _make_auth_header(self.personal_access_token)
