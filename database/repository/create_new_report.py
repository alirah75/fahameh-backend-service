from sqlalchemy.orm import Session
from schemas.Reports import ReportCreate
from database.models.T_Reports import Reports
from core.config import settings

def insert_new_report(db: Session, data: ReportCreate):
    new_report = Reports(
            RFI_Numbering=data.rfi_numbering,
            Report_No=data.report_no,
            RevNO=data.rev_no,
            Doc_Status=data.Doc_Status,
            IssueDate=data.IssueDate,
            Remark=data.Remark,
            App_manday_1stPrice=data.App_manday_1stPrice,
            UnitNo=data.UnitNo,
            VendorName=data.VendorName,
            IRNNO=data.IRNNO,
            SRNNO=data.SRNNo,
            User=data.user,
            DateShamsi=settings.gregorian_to_jalali_str(data.IssueDate)
        )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
