from typing import Annotated

from core import InvalidCredentialsException, UserAlreadyExistsException
from dependencies import get_auth_service
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Token, UserCreate, UserLogin, UserResponse
from services import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserResponse:
    try:
        user = await service.register(data)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    return UserResponse.model_validate(user)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    credentials: UserLogin,
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> Token:
    try:
        token = await service.login(credentials)
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return Token(access_token=token)
