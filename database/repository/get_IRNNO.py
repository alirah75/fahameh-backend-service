from sqlalchemy.orm import Session
from database.models.T_Invoice import Invoice
from database.models.T_TimeTable import TimeTable
from database.models.T_Reports import Reports
from database.models.T_Project import Project


def get_project_last_irnn(db: Session, project_name: str, Over_Domestic: str):
    project = db.query(Project).filter(Project.Title == project_name).first()
    if not project:
        return {"error": "Project not found"}

    idp = project.IDP

    invoice = db.query(Invoice).filter(
        Invoice.IDP == idp,
        Invoice.Over_Domestic == Over_Domestic
    ).first()

    if not invoice:
        return {"error": "Project not found in Invoice table"}

    idom = invoice.IDOM

    timetable_rows = db.query(TimeTable).filter(
        TimeTable.IDP == idp,
        TimeTable.IDOM == idom
    ).all()

    if not timetable_rows:
        return {"error": "No TimeTable rows found"}

    rfi_numbers = [row.RFI_Numbering for row in timetable_rows]

    # لیست برای نگهداری همه مقادیر IRNNO
    all_irnno_values = []

    # گرفتن همه گزارش‌ها و استخراج بزرگترین مقدار از هر IRNNO
    for rfi in rfi_numbers:
        reports = db.query(Reports).filter(
            Reports.RFI_Numbering == rfi
        ).all()

        for rep in reports:
            if rep.IRNNO:
                # مثال: "12/13/54/80"
                parts = rep.IRNNO.split("/")
                # تبدیل به عدد و حذف موارد غیر عددی
                nums = []
                for p in parts:
                    p = p.strip()
                    if p.isdigit():
                        nums.append(int(p))

                if nums:
                    max_num = max(nums)
                    all_irnno_values.append(max_num)

    if not all_irnno_values:
        all_irnno_values.append(0)

    # بزرگ‌ترین عدد نهایی
    final_max_irnno = max(all_irnno_values)

    return {"irnno": final_max_irnno, "next_irnno": final_max_irnno + 1}

