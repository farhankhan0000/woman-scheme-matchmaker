import os
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, AsyncSession)
from collections.abc import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from pathlib import Path
from typing import Annotated
from fastapi import Depends

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from the root .env file")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True,
                       pool_recycle=300)

SessionLocal = async_sessionmaker(class_=AsyncSession, bind=engine, autocommit = False, autoflush=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())

db_dependency = Annotated[AsyncSession, Depends(get_db)]