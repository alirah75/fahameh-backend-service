from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.config import settings
from database.models.T_RFIDate import RFI_Date
from database.models.T_Reports import Reports
from database.models.T_TimeTable import TimeTable



def delete_notification_service(db: Session, rfi_number: str):
    try:
        rfi_date_rows = db.query(RFI_Date).filter(RFI_Date.RFI_Numbering == rfi_number).all()

        for row in rfi_date_rows:
            db.delete(row)

        report_rows = db.query(Reports).filter(Reports.RFI_Numbering == rfi_number).all()

        for report in report_rows:
            db.delete(report)

        time_table_rows = db.query(TimeTable).filter(TimeTable.RFI_Numbering == rfi_number).first()
        db.delete(time_table_rows)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete notification data: {str(e)}"
        )

def delete_one_date_service(db: Session, rfi_number: str, date_):

    date = date_.date_
    date_rows = db.query(RFI_Date).filter(RFI_Date.RFI_Numbering == rfi_number,
                                              RFI_Date.RFI_Date == date).first()
    db.delete(date_rows)
    db.commit()
