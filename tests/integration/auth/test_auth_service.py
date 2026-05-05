import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from tests.fixtures.users.user_model import EXIST_GOOGLE_USER_ID, EXISTS_GOOGLE_USER_EMAIL

pytestmark = pytest.mark.asyncio


# async def test_google_auth__login_not_exist_user(auth_service, db_session):
#     session: AsyncSession = db_session
#     code = "fake_code"
    
#     async with session as session:
#         users = (await session.execute(select(UserProfile))).scalars().all()
        
#     user = await auth_service.google_auth(code)
    
#     assert len(users) == 0
#     assert user is not None
#     async with session as session:
#         login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()
        
#     assert login_user is not None
    
    
async def test_google_auth__login_exists_user(auth_service, db_session):
    query = insert(UserProfile).values(
        id=EXIST_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL
    )
    session = db_session
    code = "fake_code"
    
    async with session as session:
        await session.execute(query)
        await session.commit()
        user_data = await auth_service.google_auth(code)

    
    async with session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id==user_data.user_id))).scalar_one_or_none()
        
    assert login_user.email == EXISTS_GOOGLE_USER_EMAIL
    assert user_data.user_id == EXIST_GOOGLE_USER_ID
    
    
async def test_base_login__success(auth_service, db_session):
    session = db_session
    username = "test_username"
    password = "test_password"
    query = insert(UserProfile).values(
        username=username,
        password=password
    )
    async with session as session:
        await session.execute(query)
        await session.commit()
    
    user_data = await auth_service.login(username=username, password=password)
    async with session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.username==username))).scalar_one_or_none()
    
    assert login_user is not None
    assert user_data.user_id == login_user.id