from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: SessionDep):
        self.session = session

    def get(self, user_id: int):
        """
        Get a specific user by id.
        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str):
        query = select(User).where(User.email == email)
        return self.session.exec(query).first()

    def create(self, entity: User) -> User:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_all(self, **kwargs):
        skip = kwargs.pop("skip")
        limit = kwargs.pop("limit")
        count = self.get_count(User, **kwargs)
        statement = self.apply_filters(
            select(User).offset(skip).limit(limit),
            User,
            **kwargs,
        )
        users = self.session.exec(statement).all()

        return users, count

    def apply_filters(self, query, model, **kwargs):
        for attr, value in kwargs.items():
            if value:
                query = query.filter(getattr(model, attr) == value)
        return query

    def get_count(self, model, **kwargs):
        query = self.apply_filters(
            select(func.count()).select_from(model),
            User,
            **kwargs,
        )
        return self.session.exec(query).one()
