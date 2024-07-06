# authentication.py

from typing import List, Optional
import pydantic
from fastapi_sso.sso.base import DiscoveryDocument, OpenID, SSOBase

class MicrosoftSSO(SSOBase):
    """Class providing login using Microsoft OAuth."""

    provider = "microsoft"
    scope: List[str] = ["openid", "User.Read", "email"]
    version = "v1.0"
    tenant: str = "common"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[pydantic.AnyHttpUrl] = None,
        allow_insecure_http: bool = False,
        use_state: bool = False,  # TODO: Remove use_state argument
        scope: Optional[List[str]] = None,
        tenant: Optional[str] = None,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            allow_insecure_http=allow_insecure_http,
            use_state=use_state,
            scope=scope,
        )
        self.tenant = tenant or self.tenant

    async def get_discovery_document(self) -> DiscoveryDocument:
        return {
            "authorization_endpoint": f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize",
            "token_endpoint": f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token",
            "userinfo_endpoint": f"https://graph.microsoft.com/{self.version}/me",
        }

    async def openid_from_response(self, response: dict) -> OpenID:
        return OpenID(
            email=response.get("mail"),
            display_name=response.get("displayName"),
            provider=self.provider,
            id=response.get("id"),
            first_name=response.get("givenName"),
            last_name=response.get("surname"),
        )
