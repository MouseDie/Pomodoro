import pytest
import asyncio


pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.users.user_model",
    "tests.fixtures.infrastructure",
]


@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр цикла событий для каждого тестового сеанса."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()