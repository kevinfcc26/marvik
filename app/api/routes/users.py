from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.models import UserCreate, UserFilter, UserPublic, UsersPublic
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/list_users",
    response_model=UsersPublic,
)
def read_users(service: Annotated[UserService, Depends()], filters: UserFilter = Depends()) -> Any:
    """
    Retrieve users.
    """
    filters_dict = filters.model_dump()
    users, count = service.get_all(**filters_dict)

    return UsersPublic(data=users, count=count)


@router.post("/create_user", response_model=UserPublic)
def create_user(service: Annotated[UserService, Depends()], user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = service.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    return service.create(user_in)
