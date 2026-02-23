from pydantic import BaseModel, Field
from typing import Optional


class DailyReportQuery(BaseModel):
    year: int = Field(..., ge=1400, le=1500, description="سال شمسی")
    month: str = Field(..., min_length=1, description="نام ماه شمسی")
    over_domestic: str = Field(default="داخلی کالا")


class DailyReportResponse(BaseModel):
    project_title: str
    month_name: str
    year: int
    personnel_code: Optional[str]
    remark: Optional[str]
    rfi_number: str
    inspector_name: str
    rfi_date: str
    date_shamsi: str
    approve_man_day: int
    inspector_price: float
    final_price: float
    total_price: float
    fix_total_price: float

    class Config:
        orm_mode = True
