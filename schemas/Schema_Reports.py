from typing import Optional

import jdatetime
from pydantic import BaseModel, validator
from datetime import date


class BaseReportSchema(BaseModel):
    rfi_numbering: Optional[str]
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
            print(v)
            # تبدیل جداکننده / به -
            v = v.replace("/", "-")
            # تبدیل Jalali به Gregorian
            year, month, day = map(int, v.split("-"))
            g_date = jdatetime.date(year, month, day).togregorian()
            return g_date
        return v


class ReportCreateSchema(BaseReportSchema):
    pass


class ReportUpdateSchema(BaseReportSchema):
    pass
