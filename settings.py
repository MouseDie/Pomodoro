import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv(dotenv_path=".local.env")

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 54321
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    #DB_DRIVER: str = 'postgresql+psycopg2'
    DB_DRIVER: str = 'postgresql+asyncpg'
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/auth/google'
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    YANDEX_CLIENT_ID: str = os.getenv('YANDEX_CLIENT_ID')
    YANDEX_SECRET_KEY: str = os.getenv('YANDEX_SECRET_KEY')
    YANDEX_REDIRECT_URI: str = 'http://localhost:8000/auth/yandex'
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"
    
    
    
    
    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    
    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    
    
    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"