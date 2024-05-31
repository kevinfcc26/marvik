from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.permissions import PermissionLevel
from app.enums.user_level import UserLevel
from app.models import UserCreate, UserFilter, UserPublic, UsersPublic
from app.services.user_service import UserService

router = APIRouter()

counter = {"list_users": 0, "create_user": 0}


@router.get(
    "/list_users",
    response_model=UsersPublic,
    dependencies=[Depends(PermissionLevel([UserLevel.ADMIN, UserLevel.USER]))],
)
def read_users(service: Annotated[UserService, Depends()], filters: UserFilter = Depends()) -> Any:
    """
    Retrieve users.
    """
    counter["list_users"] += 1
    filters_dict = filters.model_dump()
    users, count = service.get_all(**filters_dict)

    return UsersPublic(data=users, count=count)


@router.post("/create_user", response_model=UserPublic, dependencies=[Depends(PermissionLevel([UserLevel.ADMIN]))])
def create_user(service: Annotated[UserService, Depends()], user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    counter["create_user"] += 1
    user = service.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    return service.create(user_in)


@router.get("/counter", response_model=dict)
def get_counter():

    return counter
