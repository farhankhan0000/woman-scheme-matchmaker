from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from backend.models import User
from passlib.context import CryptContext
from backend.database import db_dependency

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")

class UserInfo(BaseModel):
    name: str=Field(min_length=1)
    user_name: str=Field(min_length=3)
    password: str=Field(min_length=8, max_length=72)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def user_signup(user_info: UserInfo, db: db_dependency):
    result = await db.execute(select(User).where(User.user_name == user_info.user_name))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    hashed_password=pwd_context.hash(user_info.password)
    user = User(name=user_info.name,
                user_name=user_info.user_name,
                password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message" : "user registered successfully",
            "user_id" : user.id}

