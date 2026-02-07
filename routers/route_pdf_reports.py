from fastapi import Depends, APIRouter, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database.repository.get_daily_report import daily_report
from database.session import get_db
from routers.route_login import get_current_user
from urllib.parse import quote
from io import BytesIO
import pandas as pd

router = APIRouter()


@router.get(
    "/daily-report/",
    summary="گزارش روزانه (لینک یا دانلود مستقیم)",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "Excel file"
        }
    }
)
def daily_report_view(
    year: int = Query(..., ge=1400, le=1500),
    month: str = Query(...),
    over_domestic: str = Query(...),
    download: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = daily_report(db=db, year=year, month=month, over_domestic=over_domestic)

    if not result:
        raise HTTPException(status_code=404, detail="گزارشی یافت نشد")

    if download:
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

    from urllib.parse import urlencode
    return {
        "download_url": "/pdf_reports/daily-report/?" + urlencode({
            "year": year,
            "month": month,
            "over_domestic": over_domestic,
            "download": True
        })
    }

def generate_daily_report_excel(data: list) -> BytesIO:
    df = pd.DataFrame(data)

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