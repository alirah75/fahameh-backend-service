from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float, Integer

from database.models.T_Project import Project
from database.models.T_Inspector import Inspector
from database.models.T_Invoice import Invoice
from database.models.T_TimeTable import TimeTable
from database.models.T_RFIDate import RFI_Date
from database.models.S_Date import S_Date
from database.models.S_DateMonthsName import DateMonthsName


def daily_report(db: Session, year: int, month: str, over_domestic: str):

    # 🔹 CAST ستون‌ها (خیلی مهم)
    final_price = cast(RFI_Date.FinalPrice, Float)
    inspector_price = cast(RFI_Date.InspectorPrice, Float)
    approve_man_day = cast(RFI_Date.ApproveManday, Integer)

    query = (
        db.query(
            Project.Title.label("project_title"),
            DateMonthsName.HejriFarsi.label("month_name"),
            func.substr(S_Date.DateShamsi, 1, 4).label("year"),
            Inspector.PersonnelCode.label("personnel_code"),
            TimeTable.Remark.label("remark"),
            RFI_Date.RFI_Numbering.label("rfi_number"),
            RFI_Date.Inspector_Name.label("inspector_name"),
            RFI_Date.RFI_Date.label("rfi_date"),
            S_Date.DateShamsi.label("date_shamsi"),
            approve_man_day.label("approve_man_day"),
            inspector_price.label("inspector_price"),
            final_price.label("final_price"),
            (final_price * approve_man_day).label("total_price"),
            (inspector_price * approve_man_day).label("fix_total_price"),
        )
        # JOIN ها
        .join(Invoice, Project.IDP == Invoice.IDP)
        .join(
            TimeTable,
            (Invoice.IDP == TimeTable.IDP) &
            (Invoice.IDOM == TimeTable.IDOM)
        )
        .join(RFI_Date, TimeTable.RFI_Numbering == RFI_Date.RFI_Numbering)
        .join(S_Date, S_Date.DateMiladi == RFI_Date.RFI_Date)
        .join(DateMonthsName, S_Date.IdMonthShamsi == DateMonthsName.IdMonth)
        .outerjoin(Inspector, Inspector.Inspector_Name == RFI_Date.Inspector_Name)

        # WHERE
        .filter(
            DateMonthsName.HejriFarsi == month,
            func.substr(S_Date.DateShamsi, 1, 4) == str(year),
            Invoice.Over_Domestic == over_domestic
        )

        # ORDER BY
        .order_by(
            RFI_Date.Inspector_Name,
            S_Date.DateShamsi
        )
    )

    return query.all()
