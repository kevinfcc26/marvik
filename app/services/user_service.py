from typing import Annotated

from fastapi import Depends

from app.models import User, UserCreate
from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.utils.security import get_password_hash


class UserService:
    def __init__(self, repository: Annotated[UserRepository, Depends()]):
        self.repository: BaseRepository = repository

    def get_all(self, **kwargs):
        return self.repository.get_all(**kwargs)

    def get_by_id(self, user_id: int):
        return self.repository.get(user_id)

    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)

    def create(self, user_create: UserCreate):
        user = User.model_validate(user_create, update={"hashed_password": get_password_hash(user_create.password)})
        return self.repository.create(user)
