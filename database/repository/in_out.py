from sqlalchemy.orm import Session
from database.models.T_Invoice import Invoice

def get_inout_list(db: Session, column_name: str):
    column = getattr(Invoice, column_name)
    results = db.query(column).distinct().all()
    return [r[0] for r in results]
