from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# import sqlite3
# from settings import Settings

# settings = Settings()

# def get_db_connection() -> sqlite3.Connection:
#     return sqlite3.connect(settings.sqlite_db_name)

#engine = create_engine("sqlite:///pomodoro.sqlite")

engine = create_engine("postgresql+psycopg2://postgres:password@localhost:54321/pomodoro")

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session

