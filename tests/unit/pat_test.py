"""Unit tests for the Tempest Personal Access Token (PAT) functionality."""
from tempestwx.pat import TempestPersonalAccessToken

class TempestPersonalAccessTokenTest:
    """Test class for TempestPersonalAccessToken."""

    def test_init(self):
        """Test the initialization of the TempestPersonalAccessToken class."""
        pat = TempestPersonalAccessToken()
        assert pat.personal_access_token is None
        assert not pat.get_auth_header()
        pat = TempestPersonalAccessToken("test_token")
        assert pat.personal_access_token == "test_token"
        assert pat.get_auth_header() == {"Authorization": "Bearer test_token"}

