import re

from sqlalchemy.orm import Session
from database.models.T_Invoice import Invoice
from database.models.T_TimeTable import TimeTable
from database.models.T_Reports import Reports
from database.models.T_Project import Project


# def get_project_last_irnn(db: Session, project_name: str, Over_Domestic: str):
#     project = db.query(Project).filter(Project.Title == project_name).first()
#     if not project:
#         return {"error": "Project not found"}
#
#     idp = project.IDP
#
#     invoice = db.query(Invoice).filter(
#         Invoice.IDP == idp,
#         Invoice.Over_Domestic == Over_Domestic
#     ).first()
#
#     if not invoice:
#         return {"error": "Project not found in Invoice table"}
#
#     idom = invoice.IDOM
#
#     timetable_rows = db.query(TimeTable).filter(
#         TimeTable.IDP == idp,
#         TimeTable.IDOM == idom
#     ).all()
#
#     if not timetable_rows:
#         return {"error": "No TimeTable rows found"}
#
#     rfi_numbers = [row.RFI_Numbering for row in timetable_rows]
#
#     # نگهداری بیشینه IRNNO و RFI_Numbering مربوطه
#     final_max_irnno = 0
#     max_rfi_numbering = None
#
#     for rfi in rfi_numbers:
#         reports = db.query(Reports).filter(
#             Reports.RFI_Numbering == rfi
#         ).all()
#
#         for rep in reports:
#             if rep.IRNNO:
#                 parts = rep.IRNNO.split("/")
#                 nums = [int(p.strip()) for p in parts if p.strip().isdigit()]
#
#                 if nums:
#                     max_num = max(nums)
#                     if max_num > final_max_irnno:
#                         final_max_irnno = max_num
#                         max_rfi_numbering = rfi
#
#     rfi_row = db.query(TimeTable).filter(
#         TimeTable.IDP == idp,
#         TimeTable.IDOM == idom,
#         TimeTable.RFI_Numbering == max_rfi_numbering
#     ).first()
#
#     rfi_numer_value = rfi_row.RFI_Number if rfi_row else None
#
#     return {
#         "irnno": final_max_irnno,
#         "next_irnno": final_max_irnno + 1,
#         "rfi_numer": rfi_numer_value
#     }


def get_project_last_irnn(db: Session, project_name: str, Over_Domestic: str):
    # پیدا کردن پروژه
    project = db.query(Project).filter(Project.Title == project_name).first()
    if not project:
        return {"error": "Project not found"}

    idp = project.IDP

    # پیدا کردن فاکتور مرتبط با پروژه و نوع
    invoice = db.query(Invoice).filter(
        Invoice.IDP == idp,
        Invoice.Over_Domestic == Over_Domestic
    ).first()
    if not invoice:
        return {"error": "Project not found in Invoice table"}

    idom = invoice.IDOM

    # گرفتن ردیف‌های TimeTable مرتبط
    timetable_rows = db.query(TimeTable).filter(
        TimeTable.IDP == idp,
        TimeTable.IDOM == idom
    ).all()
    if not timetable_rows:
        return {"error": "No TimeTable rows found"}

    rfi_numbers = [row.RFI_Numbering for row in timetable_rows]

    # نگهداری بیشینه IRNNO و RFI_Numbering مربوطه
    final_max_irnno = 0
    max_rfi_numbering = None

    # بررسی همه RFI_Numbering ها
    for rfi in rfi_numbers:
        reports = db.query(Reports).filter(
            Reports.RFI_Numbering == rfi
        ).all()

        for rep in reports:
            if rep.IRNNO:
                # پیدا کردن تمام اعداد موجود در رشته IRNNO (هم با / و هم با فاصله)
                nums = [int(num) for num in re.findall(r'\d+', rep.IRNNO)]
                if nums:
                    max_num = max(nums)
                    if max_num > final_max_irnno:
                        final_max_irnno = max_num
                        max_rfi_numbering = rfi

    # پیدا کردن ردیف TimeTable مربوط به بیشینه IRNNO
    rfi_row = db.query(TimeTable).filter(
        TimeTable.IDP == idp,
        TimeTable.IDOM == idom,
        TimeTable.RFI_Numbering == max_rfi_numbering
    ).first()

    rfi_numer_value = rfi_row.RFI_Number if rfi_row else None

    return {
        "irnno": final_max_irnno,
        "next_irnno": final_max_irnno + 1,
        "rfi_numer": rfi_numer_value
    }