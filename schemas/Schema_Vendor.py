from pydantic import BaseModel
from typing import Optional

class VendorBase(BaseModel):
    name: str
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    over_domestic: Optional[bool] = None


class VendorCreate(VendorBase):
    name: str


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    over_domestic: Optional[bool] = None


class VendorRead(VendorBase):
    id: int

    class Config:
        orm_mode = True
