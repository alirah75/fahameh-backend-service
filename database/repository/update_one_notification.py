from sqlalchemy.orm import Session
from database.models.T_TimeTable import TimeTable
from schemas.TimeTable import TimeTableUpdate

def update_notif(db: Session, rfi_number: str, payload: TimeTableUpdate, current_user: str):
    record = db.query(TimeTable).filter(TimeTable.RFI_Numbering == rfi_number).first()

    if not record:
        return None

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    # در صورت نیاز ثبت آپدیت‌کننده
    if hasattr(record, "Updated_By"):
        record.Updated_By = current_user

    db.commit()
    db.refresh(record)

    return record
