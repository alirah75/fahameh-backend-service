import jdatetime
from pydantic import BaseModel, validator
from datetime import date
from typing import List, Optional


def parse_jalali(v):
    """تبدیل تاریخ شمسی به میلادی"""
    if v is None:
        return v

    def convert(item):
        if isinstance(item, str):
            item = item.replace("/", "-")
            year, month, day = map(int, item.split("-"))
            return jdatetime.date(year, month, day).togregorian()
        return item

    if isinstance(v, list):
        return [convert(item) for item in v]
    return convert(v)


class TimeTableCreate(BaseModel):
    IDP: int
    IDOM: int
    IDR: int = None
    InspectionDate: Optional[List[date]]
    Over_Domestic: Optional[str]
    InspectionLocation: Optional[str]
    RFI_Number: Optional[str]
    RFI_Recived_Date: Optional[date]
    RFI_Status: Optional[str]
    VendorName: Optional[str]
    Inspection_Duration: Optional[str]
    Inspector_Name: Optional[str]
    Remark: Optional[str] = None
    QTY_3rdpartinspector: Optional[str] = None
    approved_Duration: Optional[str] = None
    Material: Optional[str] = None
    User_Name: Optional[str]
    FolderNo: Optional[str] = None
    NotificationNo: Optional[str] = None
    DateShamsi: Optional[str] = None
    Inspector_Type: Optional[str] = None
    Goods_Description: Optional[str] = None
    FinalPrice: Optional[str]

    @validator("InspectionDate", "RFI_Recived_Date", pre=True)
    def validate_dates(cls, v):
        return parse_jalali(v)


class RFI_Date_Update(BaseModel):
    ApproveManday: int
    IDRD: int
    InspectorPrice: float


class Notification_Update(BaseModel):
    NotificationNo: Optional[str]
    RFI_Status: Optional[str]
    Inspector_Type: Optional[str]
    Goods_Description: Optional[str]
    RFI_Recived_Date: Optional[date]
    InspectionLocation: Optional[str]
    InspectionDate: Optional[date]
    VendorName: Optional[str]
    approved_Duration: Optional[str]
    Inspector_Name: Optional[str]
    Remark: Optional[str]
    FolderNo: Optional[str]

    @validator("InspectionDate", "RFI_Recived_Date", pre=True)
    def validate_dates(cls, v):
        return parse_jalali(v)