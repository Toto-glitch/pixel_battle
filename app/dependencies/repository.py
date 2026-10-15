from typing import Annotated

from core import get_session
from fastapi import Depends
from repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepository:
    return UserRepository(session)
