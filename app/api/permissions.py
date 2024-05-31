from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.enums.user_level import UserLevel
from app.models import User


class PermissionLevel:
    def __init__(self, required_permissions: list[UserLevel]):
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_user)):
        if user.user_level not in self.required_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
