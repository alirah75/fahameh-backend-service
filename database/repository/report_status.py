from sqlalchemy import distinct
from sqlalchemy.orm import Session
from database.models.T_Reports import Reports

def get_all_report_statuses(db: Session):
    return (db.query(distinct(Reports.Doc_Status))
        .filter(
            Reports.Doc_Status.isnot(None),
            Reports.Doc_Status.notin_(['', 'string'])
        )
        .order_by(Reports.Doc_Status.asc())
        .all()
    )
