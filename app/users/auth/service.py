from dataclasses import dataclass
import datetime as dt
from datetime import timedelta
import datetime
from jose import JWTError, jwt

from app.users.auth.client import GoogleClient, YandexClient, MailClient
from app.exception import TokenExpired, TokenNotCorrect, UserNotFoundException, UserNotCorrectPasswordException
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository.user import UserRepository
from app.users.user_profile.schema import UserLoginSchema, UserCreateSchema
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient
    
    
    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)
        
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        
        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        self.mail_client.send_welcome_email(to=user_data.email)
        #print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
        #print(user_data)
        
        
    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code)
       # print(user_data)
        
        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        self.mail_client.send_welcome_email(to=user_data.default_email)
        #print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
        
    
    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url
    
    
    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url
    
    
    def get_yandex_auth(self, code: str):
        print(code)
        
    
    
    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    #статические методы не обращаются к дргуим атрибутам класса
    @staticmethod   
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        
   
    def generate_access_token(self, user_id: int) -> str:
    #     expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
    #    # return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))
    #     token = jwt.encode(
    #         {'user_id': user_id, 'expire':expires_date_unix}, 
    #         key=self.settings.JWT_SECRET_KEY, 
    #         algorithm=self.settings.JWT_ENCODE_ALGORITHM
    #     )
    #     return token
        payload = {
            "user_id": user_id,
            "expire": (dt.datetime.now(tz=dt.UTC) + timedelta(days=7)).timestamp()
        }
        encoded_jwt = jwt.encode(payload, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return encoded_jwt
    
    
    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
       # print(payload)
        return payload['user_id']
    
    
