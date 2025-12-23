from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.session import get_db

from database.repository.in_out import get_inout_list
from database.repository.report_status import get_all_report_statuses
from routers.route_login import get_current_user


router = APIRouter()


@router.get("/report-statuses", summary="دریافت لیست وضعیت‌های ممکن برای گزارش‌ها")
def list_report_statuses(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    statuses = get_all_report_statuses(db)

    if not statuses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ وضعیت گزارشی یافت نشد"
        )

    return {idx: status[0] for idx, status in enumerate(statuses, start=1)}


@router.get("/", summary="دریافت لیست مقدارهای غیرتکراری Cmbinout از جدول T_Invoice")
def list_inout(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    values = get_inout_list(db, column_name="Over_Domestic")

    if not values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ مقداری یافت نشد"
        )

    return {i: val for i, val in enumerate(values)}
