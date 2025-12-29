from sqlalchemy.orm import Session

from database.models import Invoice
from database.models.T_TimeTable import TimeTable
from schemas.TimeTable import TimeTableCreate
from core.config import settings


def insert_in_timetable(db: Session, data: TimeTableCreate):
    rfi_numbering = create_rfi_numbering(db, data.IDP, data.IDOM)

    timetable = TimeTable(
        IDP=data.IDP,
        IDOM=data.IDOM,
        IDR=generate_idr(db, data.IDP, data.IDOM),
        RFI_Numbering=rfi_numbering,
        InspectionDate=data.InspectionDate[0],# تاریخ بازرسی
        Over_Domestic=data.Over_Domestic,# داخلی کالا یا خارجی
        InspectionLocation=data.InspectionLocation,#مان مقدار city
        RFI_Number=data.RFI_Number,# مقدار شماره نوتیفیکیشن
        RFI_Recived_Date=data.RFI_Recived_Date,#تاریخ دریافت نوتیفیکیشن
        RFI_Status=data.RFI_Status,#وضعیت که معمولا در حال انجام باید باشد
        VendorName=data.VendorName,# نام وندور
        Inspection_Duration=data.Inspection_Duration,# تعداد روز بازدید
        Inspector_Name=data.Inspector_Name,# نام بازرس
        Remark=data.Remark,# میتواند خالی باشد
        QTY_3rdpartinspector=data.QTY_3rdpartinspector,# معمولا مقدار 0 دارد
        approved_Duration=data.approved_Duration,# معمولا مقدار 0 دارد
        Material=data.Material,# معمولا مقدار خالی دارد
        User_Name=data.User_Name,# نام یوزر
        FolderNo=data.RFI_Number,# همان مقدار RFI_Number
        NotificationNo=rfi_numbering,# نمیدانم باید بپرسم. یک رشته است
        DateShamsi=settings.gregorian_to_jalali_str(data.RFI_Recived_Date),# تاریخ شمسی
        Inspector_Type=data.Inspector_Type,# یا freelance است یا resident
        Goods_Description=data.Goods_Description,# میتواند خالی باشد در هنگام ادیت مقدار بگیرد. یک رشته است
    )

    db.add(timetable)
    db.commit()
    db.refresh(timetable)
    return timetable, rfi_numbering


def create_rfi_numbering(db: Session, idp: int, idom: int):
    last = (
        db.query(TimeTable)
        .filter(TimeTable.IDP == idp, TimeTable.IDOM == idom)
        .order_by(TimeTable.RFI_Numbering.desc())
        .first()
    )

    if last and last.RFI_Numbering:
        parts = last.RFI_Numbering.split('-')
        number_str = parts[-1]  # '0080'
        number_int = int(number_str) + 1
        new_number_str = str(number_int).zfill(len(number_str))

        parts[-1] = new_number_str
        return "-".join(parts)
    else:
        invoice = db.query(Invoice).filter(Invoice.IDOM == idom).first()
        project_code = invoice.ProjectCode if invoice else "DEFAULT"
        return f"FAH-INS-{project_code}"

def generate_idr(db, idp, idom):
    last_row = (
        db.query(TimeTable)
        .filter(TimeTable.IDP == idp, TimeTable.IDOM == idom)
        .order_by(TimeTable.IDR.desc())
        .first()
    )

    return 1 if last_row is None else last_row.IDR + 1
