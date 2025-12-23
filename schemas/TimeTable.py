import jdatetime
from pydantic import BaseModel, validator
from datetime import date
from typing import List, Optional


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
    def parse_jalali_date(cls, v):
        if v is None:
            return v

        def convert(v):
            if isinstance(v, str):
                v = v.replace("/", "-")
                year, month, day = map(int, v.split("-"))
                return jdatetime.date(year, month, day).togregorian()
            return v

        # اگر لیست باشد
        if isinstance(v, list):
            return [convert(item) for item in v]

        # اگر مقدار تکی باشد
        return convert(v)


class TimeTableUpdate(BaseModel):
    pass
