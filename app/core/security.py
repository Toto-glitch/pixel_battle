from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from .config import settings
from .exceptions import TokenException

password_hasher = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(
        payload=payload,
        key=settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm]
        )
        return int(payload["sub"])
    except jwt.InvalidTokenError as e:
        raise TokenException from e
