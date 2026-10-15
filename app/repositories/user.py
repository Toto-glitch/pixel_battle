from models import User
from sqlalchemy import select

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_username(self, username: str) -> User | None:
        query = select(self.model).filter_by(username=username)
        result = await self._session.execute(query)
        model_instanse = result.scalar_one_or_none()
        return model_instanse

    async def get_by_email(self, email: str) -> User | None:
        query = select(self.model).filter_by(email=email)
        result = await self._session.execute(query)
        model_instanse = result.scalar_one_or_none()
        return model_instanse
