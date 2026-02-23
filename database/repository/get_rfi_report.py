from sqlalchemy.orm import Session

from database.models.T_TimeTable import TimeTable
from database.models.T_Reports import Reports
from database.models.T_Project import Project
from database.models.T_Invoice import Invoice


# def get_report_rfi(project_name: str, db: Session):
#     data = (
#         db.query(
#             TimeTable.RFI_Number,
#             TimeTable.RFI_Status,
#             TimeTable.InspectionDate,
#             Reports.Report_No,
#             Reports.IRNNO,
#             TimeTable.Inspection_Duration,
#             TimeTable.NotificationNo,
#             TimeTable.RFI_Numbering,
#             Project.Title,
#             Invoice.Over_Domestic,
#             TimeTable.VendorName
#         )
#         .join(Invoice, (Invoice.IDP == TimeTable.IDP) & (Invoice.IDOM == TimeTable.IDOM))
#         .join(Project, Project.IDP == Invoice.IDP)
#         .outerjoin(Reports, Reports.RFI_Numbering == TimeTable.RFI_Numbering)
#         .filter(Project.Title == project_name)
#         .all()
#     )
#     return data

# def get_report_rfi(project_name: str, project_type: str, db: Session):
#     data = (
#         db.query(
#             TimeTable.RFI_Number,
#             TimeTable.RFI_Status,
#             TimeTable.InspectionDate,
#             Reports.Report_No,
#             Reports.IRNNO,
#             TimeTable.Inspection_Duration,
#             TimeTable.NotificationNo,
#             TimeTable.RFI_Numbering,
#             Project.Title,
#             Invoice.Over_Domestic,
#             TimeTable.VendorName
#         )
#         .join(Invoice, (Invoice.IDP == TimeTable.IDP) & (Invoice.IDOM == TimeTable.IDOM) & (Invoice.Over_Domestic == project_type))
#         .join(Project, Project.IDP == Invoice.IDP)
#         .outerjoin(Reports, Reports.RFI_Numbering == TimeTable.RFI_Numbering)
#         .filter(Project.Title == project_name)
#         .all()
#     )
#     return data

# from sqlalchemy import func, and_
#
# def get_report_rfi(project_name: str, project_type: str, db: Session):
#
#     # ساب‌کوئری برای گرفتن آخرین گزارش هر RFI بر اساس IDRE
#     latest_report_subq = (
#         db.query(
#             Reports.RFI_Numbering,
#             func.max(Reports.IDRE).label("max_idre")  # 👈 ستون IDRE
#         )
#         .group_by(Reports.RFI_Numbering)
#         .subquery()
#     )
#
#     data = (
#         db.query(
#             TimeTable.RFI_Number,
#             TimeTable.RFI_Status,
#             TimeTable.InspectionDate,
#             Reports.Report_No,
#             Reports.IRNNO,
#             TimeTable.Inspection_Duration,
#             TimeTable.NotificationNo,
#             TimeTable.RFI_Numbering,
#             Project.Title,
#             Invoice.Over_Domestic,
#             TimeTable.VendorName
#         )
#         .distinct()  # 👈 معادل SELECT DISTINCT
#         .join(
#             Invoice,
#             and_(
#                 Invoice.IDP == TimeTable.IDP,
#                 Invoice.IDOM == TimeTable.IDOM,
#                 Invoice.Over_Domestic == project_type
#             )
#         )
#         .join(Project, Project.IDP == Invoice.IDP)
#
#         # جوین به ساب‌کوئری
#         .outerjoin(
#             latest_report_subq,
#             latest_report_subq.c.RFI_Numbering == TimeTable.RFI_Numbering
#         )
#
#         # جوین به خود جدول Reports با بزرگ‌ترین IDRE
#         .outerjoin(
#             Reports,
#             and_(
#                 Reports.RFI_Numbering == latest_report_subq.c.RFI_Numbering,
#                 Reports.IDRE == latest_report_subq.c.max_idre
#             )
#         )
#
#         .filter(Project.Title == project_name)
#         .all()
#     )
#
#     return data


def get_report_rfi(project_name: str, project_type: str, db: Session):
    data = (
        db.query(
            TimeTable.RFI_Number,
            TimeTable.RFI_Status,
            TimeTable.InspectionDate,
            Reports.Report_No,
            Reports.IRNNO,
            TimeTable.Inspection_Duration,
            TimeTable.NotificationNo,
            TimeTable.RFI_Numbering,
            Project.Title,
            Invoice.Over_Domestic,
            TimeTable.VendorName
        )
        .distinct()
        .join(
            Invoice,
            (Invoice.IDP == TimeTable.IDP) &
            (Invoice.IDOM == TimeTable.IDOM) &
            (Invoice.Over_Domestic == project_type)
        )
        .join(Project, Project.IDP == Invoice.IDP)
        .outerjoin(Reports, Reports.RFI_Numbering == TimeTable.RFI_Numbering)
        .filter(Project.Title == project_name)
        .all()
    )
    return data