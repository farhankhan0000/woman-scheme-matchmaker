from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserInfo(BaseModel):
    name: str=Field(min_length=1)
    user_name: str=Field(min_length=3)
    password: str=Field(min_length=8, max_length=72)




