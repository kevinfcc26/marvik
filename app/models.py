from sqlmodel import Field, SQLModel

from app.enums.user_level import UserLevel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str | None = None
    surname: str
    user_level: UserLevel = UserLevel.GUEST
    is_active: bool = True
    is_superuser: bool = False


class UserFilter(SQLModel):
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    user_level: UserLevel | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    skip: int = 0
    limit: int = 100


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
