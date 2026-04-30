#from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
#from sqlalchemy.orm import sessionmaker

from app.settings import Settings


settings = Settings()

#engine = create_engine("postgresql+psycopg2://postgres:password@localhost:54321/pomodoro")
engine = create_async_engine(
    settings.db_url,
    future=True,
    echo=True,
    pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

#Session = sessionmaker(engine)

# def get_db_session() -> Session:
#     return Session


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session