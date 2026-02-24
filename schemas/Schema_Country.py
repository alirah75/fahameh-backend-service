from pydantic import BaseModel
from typing import Optional

class CountryBase(BaseModel):
    title: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    title: Optional[str] = None


class CountryRead(CountryBase):
    id: int

    class Config:
        orm_mode = True