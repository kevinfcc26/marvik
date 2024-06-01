from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.enums.user_level import UserLevel
from app.models import User, UserCreate
from app.utils.security import get_password_hash

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:

    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_create = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            user_level=UserLevel.ADMIN,
            surname=settings.FIRST_SUPERUSER_SURNAME,
        )
        user = User.model_validate(user_create, update={"hashed_password": get_password_hash(user_create.password)})
        session.add(user)
        session.commit()
