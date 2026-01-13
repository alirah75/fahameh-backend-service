from pydantic import BaseModel


class VendorCreateSchema(BaseModel):
    name: str
    over_domestic: bool