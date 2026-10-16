from typing import Annotated

from core import get_session
from fastapi import Depends
from repositories import UserRepository
from services import AuthService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthService:
    repo = UserRepository(session)
    return AuthService(repo)
