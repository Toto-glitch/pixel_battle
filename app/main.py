from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from core import close_db_connection, close_redis_connection, settings
from fastapi import FastAPI
from routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("starting app...")
    yield
    print("closing app...")
    await close_redis_connection()
    await close_db_connection()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.uc.host,
        port=settings.uc.port,
        reload=settings.uc.reload
    )
