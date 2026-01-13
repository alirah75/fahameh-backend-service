from database.models import Reports
from sqlalchemy.orm import Session

from schemas.Reports import ReportUpdateSchema


def update_report(db: Session, rfi_number: str, data: ReportUpdateSchema):
    obj = db.query(Reports)\
        .filter(Reports.RFI_Numbering == rfi_number)\
        .first()

    if not obj:
        return None

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)

    return obj
