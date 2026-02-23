from pydantic import BaseModel, Field
from typing import Optional


class UserBaseSchema(BaseModel):
    user_name: str
    password: str
    permit: str
    unit: str


class UserCreateSchema(UserBaseSchema):
    password: str

class UserReadSchema(BaseModel):
    id: int
    user_name: str
    permit: Optional[str] = None
    unit: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None
    permit: Optional[str] = None
    unit: Optional[str] = None
