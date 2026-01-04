from sqlalchemy.orm import Session

from database.models.T_TimeTable import TimeTable
from database.models.T_Reports import Reports
from database.models.T_Project import Project
from database.models.T_Invoice import Invoice


def get_report_rfi(project_name: str, db: Session):
    data = (
        db.query(
            TimeTable.RFI_Number,
            TimeTable.RFI_Status,
            TimeTable.InspectionDate,
            Reports.Report_No,
            Reports.IRNNO,
            TimeTable.Inspection_Duration,
            TimeTable.NotificationNo,
            Project.Title,
            Invoice.Over_Domestic,
            TimeTable.VendorName
        )
        .join(Invoice, (Invoice.IDP == TimeTable.IDP) & (Invoice.IDOM == TimeTable.IDOM))
        .join(Project, Project.IDP == Invoice.IDP)
        .outerjoin(Reports, Reports.RFI_Numbering == TimeTable.RFI_Numbering)
        .filter(Project.Title == project_name)
        .all()
    )
    return data
