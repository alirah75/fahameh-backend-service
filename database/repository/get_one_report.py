from sqlalchemy.orm import Session
from database.models.T_Reports import Reports

def find_report(db: Session, rfi_number: str):

    # if report_number:
    #     last = db.query(Reports).filter(
    #         Reports.RFI_Numbering == rfi_number,
    #         Reports.Report_No == report_number
    #     ).first()
    #     return last
    # else:
    last = db.query(Reports).filter(
        Reports.RFI_Numbering.ilike(f"%{rfi_number}%")
    ).all()
    return last
