from pydantic import BaseModel


class VendorCreate(BaseModel):
    name: str
    over_domestic: bool