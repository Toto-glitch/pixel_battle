from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from models import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, db_session: AsyncSession) -> None:
        self._session = db_session

    async def add(self, **kwargs: Any) -> T:
        model_instanse = self.model(**kwargs)
        self._session.add(model_instanse)
        await self._session.flush()
        await self._session.refresh(model_instanse)
        return model_instanse

    async def all(self, offset: int = 0, limit: int = 10) -> Sequence[T]:
        query = select(self.model).offset(offset).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get(self, object_id: int) -> T | None:
        query = select(self.model).filter_by(id=object_id)
        result = await self._session.execute(query)
        model_instanse = result.scalar_one_or_none()
        return model_instanse

    async def remove(self, model_instanse: T) -> None:
        await self._session.delete(model_instanse)
        await self._session.flush()
