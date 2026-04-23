from sqlalchemy.orm import declarative_base

from settings import Settings


settings = Settings()


# import sqlite3
# from settings import Settings

# settings = Settings()

# def get_db_connection() -> sqlite3.Connection:
#     return sqlite3.connect(settings.sqlite_db_name)

#engine = create_engine("sqlite:///pomodoro.sqlite")

engine = create_engine(settings.db_url)

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session

