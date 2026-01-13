from typing import Optional

import jdatetime
from pydantic import BaseModel, validator
from datetime import date


class ReportCreateSchema(BaseModel):
    rfi_numbering: str
    report_no: Optional[str]
    rev_no: Optional[str] = None

    IssueDate: Optional[date]
    Doc_Status: Optional[str]

    Remark: Optional[str] = None
    App_manday_1stPrice: Optional[int] = 1

    UnitNo: Optional[str] = None
    VendorName: Optional[str]
    IRNNO: Optional[str] = None
    SRNNo: Optional[str] = None

    user: str
    DateShamsi: Optional[str] = None

    @validator("IssueDate", pre=True)
    def parse_jalali_date(cls, v):
        if isinstance(v, str):
            # تبدیل جداکننده / به -
            v = v.replace("/", "-")
            # تبدیل Jalali به Gregorian
            year, month, day = map(int, v.split("-"))
            g_date = jdatetime.date(year, month, day).togregorian()
            return g_date
        return v


class ReportUpdateSchema(BaseModel):
    rfi_numbering: Optional[str] = None
    report_no: Optional[str] = None
    rev_no: Optional[str] = None

    IssueDate: Optional[date] = None
    Doc_Status: Optional[str] = None

    Remark: Optional[str] = None
    App_manday_1stPrice: Optional[int] = None

    UnitNo: Optional[str] = None
    VendorName: Optional[str] = None
    IRNNO: Optional[str] = None
    SRNNo: Optional[str] = None

    user: Optional[str] = None
    DateShamsi: Optional[str] = None

    @validator("IssueDate", pre=True)
    def parse_jalali_date(cls, v):
        if isinstance(v, str):
            # تبدیل جداکننده / به -
            v = v.replace("/", "-")
            # تبدیل Jalali به Gregorian
            year, month, day = map(int, v.split("-"))
            g_date = jdatetime.date(year, month, day).togregorian()
            return g_date
        return v
