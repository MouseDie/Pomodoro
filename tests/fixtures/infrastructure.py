import pytest
import pytest_asyncio
from app.settings import Settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.infra.database.database import Base




@pytest.fixture
def settings():
    return Settings()



@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_models(event_loop):
    # Создаем engine внутри фикстуры, чтобы он использовал правильный event_loop
    engine = create_async_engine(
        url='postgresql+asyncpg://postgres:password@localhost:54322/pomodoro-test',
        future=True,
        echo=True,
        pool_pre_ping=True
    )
    
    # эта часть запускается перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # запускается по окончании тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Закрываем пул соединений
    await engine.dispose()

# engine = create_async_engine(
#     url='postgresql+asyncpg://postgres:password@localhost:54322/pomodoro-test',
#     future=True,
#     echo=True,
#     pool_pre_ping=True
# )

# AsyncSessionFactory = async_sessionmaker(
#     engine,
#     autoflush=False,
#     expire_on_commit=False
# )


@pytest_asyncio.fixture()
async def db_session():
    # Создаем новый engine для каждой сессии или используем один на session
    engine = create_async_engine(
        url='postgresql+asyncpg://postgres:password@localhost:54322/pomodoro-test',
        future=True,
        echo=True,
        pool_pre_ping=True
    )
    
    AsyncSessionFactory = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False
    )
    
    async with AsyncSessionFactory() as session:
        yield session
    
    await engine.dispose()
