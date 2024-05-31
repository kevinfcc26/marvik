from abc import ABC, abstractmethod
from typing import TypeVar

from sqlmodel import Session

T = TypeVar("T")


class BaseRepository(ABC):
    session: Session

    @abstractmethod
    def get_all(self, **kwargs):
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get(self, user_id: int) -> T:
        pass
