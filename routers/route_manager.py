from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.repository.get_daily_report import daily_report
from database.session import get_db
from routers.route_login import get_current_user


router = APIRouter()


@router.get(
    "/financial-summary/",
    summary="نمایش اطلاعات مالی برای مدیر",
    status_code=status.HTTP_200_OK,
    response_description="Financial summary data for the manager"
)
def get_financial_summary(
    year: int = Query(..., ge=1400, le=1500, description="سال مورد نظر"),
    month: str = Query(..., description="ماه مورد نظر"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    این API اطلاعات مالی مدیر را بر اساس سال و ماه بازمی‌گرداند.
    """
    result = daily_report(db=db, year=year, month=month, over_domestic='داخلی کالا')

    if not result:
        raise HTTPException(status_code=404, detail="هیچ داده مالی‌ای یافت نشد")

    keys = [
        "نام پروژه", "ماه", "سال", "کد پرسنلی", "توضیحات",
        "شماره RFI", "نام بازرس", "تاریخ RFI", "تاریخ شمسی",
        "نفر-روز", "هزینه بازرسی", "قیمت نهایی", "مبلغ کل", "مبلغ ثابت"
    ]

    formatted_result = [dict(zip(keys, row)) for row in result]

    return formatted_result
    # return JSONResponse(content={"year": year, "month": month, "data": formatted_result})