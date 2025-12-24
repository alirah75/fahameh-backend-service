from sqlalchemy.orm import Session
from database.models.T_RFIDate import RFI_Date
from schemas.TimeTable import RFI_Date_Update

def update_notif(db: Session, rfi_number: str, payload: RFI_Date_Update, current_user: str):
    record = db.query(RFI_Date).filter(RFI_Date.IDRD == payload.IDRD, RFI_Date.RFI_Numbering == rfi_number).first()

    if not record:
        return None

    update_data = payload.dict()

    for key, value in update_data.items():
        setattr(record, key, value)

    # در صورت نیاز ثبت آپدیت‌کننده
    if hasattr(record, "Updated_By"):
        record.Updated_By = current_user

    db.commit()
    db.refresh(record)

    return record
