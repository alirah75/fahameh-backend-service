from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.repository.pdf_reports import get_daily_report
from database.session import get_db

router = APIRouter()

@router.get('/daily-report/', summary='گزارش روزانه پروژه', status_code=status.HTTP_200_OK)
def get_daily_report_view(project_name, db: Session = Depends(get_db)):
    daily_report = get_daily_report(db, project_name)
    if not daily_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'گزارش روزانه برای تاریخ "{project_name}" پیدا نشد.'
        )
    return daily_report
