from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
    reload: bool = True


class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class CanvasConfig(BaseModel):
    width: int = Field(100, gt=0)
    height: int = Field(100, gt=0)
    cooldown_seconds: int = Field(5, gt=0)


class Settings(BaseSettings):
    uc: UvicornConfig
    db: DatabaseConfig
    redis: RedisConfig
    jwt: JWTConfig
    canvas: CanvasConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__"
    )


settings = Settings()
