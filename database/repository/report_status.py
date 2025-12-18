from sqlalchemy.orm import Session
from database.models.T_Reports import Reports

def get_all_report_statuses(db: Session):
    return db.query(Reports).order_by(Reports.IDRE.asc()).all()
