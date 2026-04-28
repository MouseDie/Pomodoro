from dataclasses import dataclass
import requests
from schema import YandexUserData
from settings import Settings



@dataclass
class YandexClient:
    settings: Settings
    
    
    def get_user_info(self, code: str):
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get("https://login.yandex.ru/info?format=json",
                                 headers={"Authorization": f"OAuth {access_token}"},
                                 verify=False)
        #print(user_info.json())
        return YandexUserData(**user_info.json(), access_token=access_token)
        #return user_info.json()
        
    
    def _get_user_access_token(self, code: str) -> str:
        
        response = requests.post(
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
            verify=False,
        )
        
        #response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        #print(response.json())
        return response.json()["access_token"]