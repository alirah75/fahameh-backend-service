from sqlalchemy.orm import Session
from database.models.T_Reports import Reports
from schemas.Reports import ReportUpdate
from core.config import settings
from fastapi import HTTPException, status

def get_report_by_rfi(db: Session, rfi_numbering: str) -> Reports:
    report = db.query(Reports).filter(Reports.RFI_Numbering == rfi_numbering).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Report with RFI "{rfi_numbering}" not found.'
        )
    return report

def update_report_fields(report: Reports, data: ReportUpdate) -> Reports:
    update_fields = data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        if field == "IssueDate" and value:
            setattr(report, "DateShamsi", settings.gregorian_to_jalali_str(value))
        setattr(report, field, value)
    return report

def commit_report_update(db: Session, report: Reports) -> Reports:
    try:
        db.commit()
        db.refresh(report)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update report: {str(e)}"
        )
    return report


def get_report_by_report_number(db: Session, report_No: str) -> Reports:
    report = db.query(Reports).filter(Reports.Report_No == report_No).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Report with RFI "{report_No}" not found.'
        )
    return report


def delete_report_commit(db: Session, report: Reports):
    try:
        db.delete(report)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )
