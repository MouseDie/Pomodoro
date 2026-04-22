from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "dfjhk23n5kb52352j23n2"
    sqlite_db_name: str  = 'pomodore.sqlite'