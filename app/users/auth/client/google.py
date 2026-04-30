from dataclasses import dataclass, field
#import requests
import httpx
from app.users.auth.schema import GoogleUserData
from app.settings import Settings



@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient = field(
        default_factory=lambda: httpx.AsyncClient(verify=False)
    )
    
    
    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        #user_info = requests.get(

        user_info = await self.async_client.get(    
            "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                #verify=False
        )
        print(user_info.json())
        return GoogleUserData(**user_info.json(), access_token=access_token)
        #return user_info.json()
        
    
    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = await self.async_client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        #print(response.json())
        return response.json()["access_token"]