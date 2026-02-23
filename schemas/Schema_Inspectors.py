from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class InspectorReadSchema(BaseModel):
    Inspector_Name: str
    PersonnelCode: str = None
    Inspector_Email: Optional[str] = None
    Inspector_phone_no: Optional[str] = None
    Location_Coverd: Optional[str] = None
    status: Optional[str] = None
    Price: Optional[Decimal] = None

    class Config:
        orm_mode = True


class InspectorCreateSchema(BaseModel):
    Inspector_Name: str
    PersonnelCode: Optional[str] = None
    Inspector_Discipline: Optional[str] = None
    Inspector_Email: Optional[str] = None
    Inspector_phone_no: Optional[str] = None
    Location_Coverd: Optional[str] = None
    status: Optional[str] = None
    Price: Optional[Decimal] = None
    OVRDom: Optional[str] = None
    Price1403: Optional[Decimal] = None


class InspectorUpdateSchema(BaseModel):
    Inspector_Name: Optional[str] = None
    PersonnelCode: Optional[str] = None
    Inspector_Discipline: Optional[str] = None
    Inspector_Email: Optional[str] = None
    Inspector_phone_no: Optional[str] = None
    Location_Coverd: Optional[str] = None
    status: Optional[str] = None
    Price: Optional[Decimal] = None
    OVRDom: Optional[str] = None
    Price1403: Optional[Decimal] = None
