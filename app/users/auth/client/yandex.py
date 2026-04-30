from dataclasses import dataclass, field
#import requests
import httpx
from app.users.auth.schema import YandexUserData
from app.settings import Settings



@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient = field(
        default_factory=lambda: httpx.AsyncClient(verify=False)
    )
    
    async def get_user_info(self, code: str):
        access_token = await self._get_user_access_token(code=code)
        #async with self.async_client as client:
        user_info = await self.async_client.get("https://login.yandex.ru/info?format=json",
                                headers={"Authorization": f"OAuth {access_token}"},
                                #verify=False
                            )
        #print(user_info.json())
        return YandexUserData(**user_info.json(), access_token=access_token)
        #return user_info.json()
        
    
    async def _get_user_access_token(self, code: str) -> str:
        
        #async with self.async_client as client:
        response = await self.async_client.post(
            self.settings.YANDEX_TOKEN_URL,
            data = {
                "code": code,
                "client_id": self.settings.YANDEX_CLIENT_ID,
                "client_secret": self.settings.YANDEX_SECRET_KEY,
                #"redirect_uri": self.settings.YANDEX_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            #verify=False,
        )
        
        #response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()["access_token"]