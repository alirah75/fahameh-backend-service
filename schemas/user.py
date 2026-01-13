from pydantic import BaseModel, Field
from typing import Optional


class UserBaseSchema(BaseModel):
    user_name: str
    password: Optional[str] = None
    permit: Optional[str] = None
    unit: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    """Schema برای ساخت کاربر جدید"""
    password: str
    unit: str = Field('QC')

class UserReadSchema(UserBaseSchema):
    """Schema برای بازگرداندن اطلاعات کاربر"""
    class Config:
        from_attributes = True
