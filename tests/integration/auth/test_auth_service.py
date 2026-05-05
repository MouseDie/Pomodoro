import pytest

pytestmark = pytest.mark.asyncio


async def test_google_auth__success(auth_service, db_session):
    code = "fake_code"
    user = await auth_service.google_auth(code)
    assert user is not None