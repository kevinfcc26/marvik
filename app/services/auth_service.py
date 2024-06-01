import logging
from typing import Annotated

from fastapi import Depends

from app.models import User
from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> User | None:
        db_user = self.user_repository.get_by_email(email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        logger.info(f"user {db_user.email} authenticated")
        return db_user
