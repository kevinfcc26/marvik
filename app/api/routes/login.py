from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUser
from app.models import Token, UserPublic, login
from app.services.auth_service import AuthService
from app.utils import security

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(auth_service: Annotated[AuthService, Depends()], data: login) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth_service.authenticate(email=data.email, password=data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return Token(access_token=security.create_access_token(user.id))


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
