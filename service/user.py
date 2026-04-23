import string
from random import random, choice
from dataclasses import dataclass

from schema import UserLoginSchema
from repository import UserRepository



@dataclass
class UserService:
    user_repository: UserRepository
    
    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self._genegate_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)
        
    @staticmethod    
    def _genegate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))