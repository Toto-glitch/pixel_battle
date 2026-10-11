import uvicorn
from core import settings
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.uc.host,
        port=settings.uc.port,
        reload=settings.uc.reload
    )
