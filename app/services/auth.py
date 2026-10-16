import asyncio

from core import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    create_access_token,
    get_password_hash,
    verify_password,
)
from models import User
from repositories import UserRepository
from schemas import UserCreate, UserLogin


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._users = user_repo

    async def register(self, data: UserCreate) -> User:
        user = await self._users.get_by(username=data.username)
        if user is not None:
            raise UserAlreadyExistsException()

        user = await self._users.get_by(email=data.email)
        if user is not None:
            raise UserAlreadyExistsException()

        hashed_password = await asyncio.to_thread(get_password_hash, data.password)
        user = await self._users.add(
            username=data.username,
            password_hash=hashed_password,
            email=data.email
        )
        return user

    async def login(self, credentials: UserLogin) -> str:
        user = await self._users.get_by(username=credentials.username)
        if user is None:
            raise InvalidCredentialsException()
        
        is_passed = await asyncio.to_thread(
            verify_password,
            plain_password=credentials.password,
            hashed_password=user.password_hash
        )
        if not is_passed:
            raise InvalidCredentialsException()
        return create_access_token(user.id)
