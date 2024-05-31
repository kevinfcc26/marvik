from enum import Enum


class UserLevel(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
