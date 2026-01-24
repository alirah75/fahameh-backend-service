from typing import Optional

import jdatetime
from pydantic import BaseModel, validator
from datetime import date


class RFI_DateSchema(BaseModel):
    date_: Optional[date]

    @validator("date_", pre=True)
    def parse_jalali_date(cls, v):
        if isinstance(v, str):
            # تبدیل جداکننده / به -
            v = v.replace("/", "-")
            # تبدیل Jalali به Gregorian
            year, month, day = map(int, v.split("-"))
            g_date = jdatetime.date(year, month, day).togregorian()
            return g_date
        return v