from sqlalchemy.orm import Session
from database.models.T_Reports import Reports

def find_report(db: Session, rfi_number: str, report_number=None):
    last = db.query(Reports).filter(
        Reports.RFI_Numbering == rfi_number,
        Reports.Report_No == report_number
    ).first()
    return last
