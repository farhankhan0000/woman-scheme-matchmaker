from fastapi import FastAPI

from backend.database import create_tables, engine
from backend.routers import users
from contextlib import asynccontextmanager
from backend import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_tables()

        yield

    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)

@app.get("/")
def health_check():
    return "hello"