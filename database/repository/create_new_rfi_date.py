from sqlalchemy import func
from sqlalchemy.orm import Session
from schemas.TimeTable import TimeTableCreate
from database.models.T_RFIDate import RFI_Date


def insert_in_rfi_date(db: Session, data: TimeTableCreate, rfi_numbering):
    rfi_dates = []


    for date in data.InspectionDate:
        idrd = generate_idrd(db)
        rfi_date = RFI_Date(
            IDRD=idrd,
            RFI_Numbering=rfi_numbering,
            RFI_Date=date,
            Inspector_Name=data.Inspector_Name,
            InspectorPrice=data.FinalPrice,
            ApproveManday=1,
            SubstituteinspectorPrice=0.0,
            FinalPrice=0,
            ApproveManday1=222

        )
        rfi_dates.append(rfi_date)
        db.add(rfi_date)
        db.commit()
    return rfi_dates


def generate_idrd(db):
    last_idr = (db.query(func.max(RFI_Date.IDRD)).scalar())
    return 1 if last_idr is None else last_idr + 1