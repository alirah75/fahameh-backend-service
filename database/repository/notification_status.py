from sqlalchemy import distinct
from sqlalchemy.orm import Session
from database.models.T_TimeTable import TimeTable

def get_all_notification_statuses(db: Session):
    return (
        db.query(distinct(TimeTable.RFI_Status))
        .filter(
            TimeTable.RFI_Status.isnot(None),
            TimeTable.RFI_Status != ''
        )
        .order_by(TimeTable.RFI_Status.asc())
        .all()
    )