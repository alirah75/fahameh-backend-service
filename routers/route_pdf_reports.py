from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from database.repository.get_daily_report import daily_report
from database.repository.pdf_reports import get_daily_report
from database.session import get_db
from routers.route_login import get_current_user
from schemas.DailyReport import DailyReportResponse
from urllib.parse import quote
import pandas as pd
from io import BytesIO


router = APIRouter()

@router.get('/daily-report/',
            response_model=List[DailyReportResponse],
            summary='گزارش گیری بر اساس سال و ماه',
            status_code=status.HTTP_200_OK)
def get_daily_report_view(
        year: int = Query(..., ge=1400, le=1500),
        month: str = Query(...),
        over_domestic: str = Query(...),
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    try:
        result = daily_report(db=db, year=year, month=month, over_domestic=over_domestic)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="گزارشی برای این ماه و سال یافت نشد")

        excel_file = generate_daily_report_excel(result)

        filename = f"daily_report_{year}_{month}.xlsx"
        encoded_filename = quote(filename)

        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای داخلی سرور: {str(e)}"
        )


def generate_daily_report_excel(data: list) -> BytesIO:
    df = pd.DataFrame(data)

    # تغییر نام ستون‌ها (اختیاری ولی حرفه‌ای)
    df.rename(columns={
        "project_title": "نام پروژه",
        "month_name": "ماه",
        "year": "سال",
        "personnel_code": "کد پرسنلی",
        "remark": "توضیحات",
        "rfi_number": "شماره RFI",
        "inspector_name": "نام بازرس",
        "rfi_date": "تاریخ RFI",
        "date_shamsi": "تاریخ شمسی",
        "approve_man_day": "نفر-روز",
        "inspector_price": "هزینه بازرس",
        "final_price": "قیمت نهایی",
        "total_price": "مبلغ کل",
        "fix_total_price": "مبلغ ثابت"
    }, inplace=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Daily Report")

    output.seek(0)
    return output