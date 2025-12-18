from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    user_name: str
    password: Optional[str] = None
    permit: Optional[str] = None
    unit: Optional[str] = None


class UserCreate(UserBase):
    """Schema برای ساخت کاربر جدید"""
    password: str
    unit: str = Field('QC')

class UserRead(UserBase):
    """Schema برای بازگرداندن اطلاعات کاربر"""
    class Config:
        from_attributes = True
