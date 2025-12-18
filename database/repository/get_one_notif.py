from sqlalchemy.orm import Session
from database.models.T_TimeTable import TimeTable
from database.models.T_RFIDate import RFI_Date

def find_notif(db: Session, rfi_number: str):
    results = db.query(TimeTable).filter(TimeTable.RFI_Numbering == rfi_number).all()

    output = []

    for timetable_row in results:
        # داده‌های TimeTable
        timetable_dict = {k: v for k, v in timetable_row.__dict__.items() if k != "_sa_instance_state"}

        # تمام ردیف‌های RFI_Date مرتبط
        rfi_dates = db.query(RFI_Date).filter(RFI_Date.RFI_Numbering == timetable_row.RFI_Numbering).all()
        rfi_list = []
        for rfi in rfi_dates:
            rfi_dict = {k: v for k, v in rfi.__dict__.items() if k != "_sa_instance_state"}
            rfi_list.append(rfi_dict)

        # ترکیب خروجی
        combined = {
            "TimeTable": timetable_dict,
            "RFI_Dates": rfi_list
        }

        output.append(combined)

    return output
