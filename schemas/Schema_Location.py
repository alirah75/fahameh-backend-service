from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class LocationBase(BaseModel):
    Overlocation: Optional[str] = None
    location: Optional[str] = None
    OverDome: Optional[str] = None
    Price: Optional[Decimal] = None
    UnitPrice: Optional[str] = None


class LocationCreate(LocationBase):
    Overlocation: str
    location: str
    OverDome: str
    Price: Decimal
    UnitPrice: str


class LocationUpdate(LocationBase):
    pass


class LocationRead(LocationBase):
    ID: int

    class Config:
        from_attributes = True