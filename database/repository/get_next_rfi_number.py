from sqlalchemy import func
from sqlalchemy.orm import Session
from database.models.T_Invoice import Invoice
from database.models.T_TimeTable import TimeTable


def get_full_rfi_info(db: Session, idp, in_out: str):
    idom = find_idom_value(db, idp, in_out)
    next_rfi = get_last_rfi_number(db, int(idp), idom, in_out)
    return idom, next_rfi


def find_idom_value(db: Session, idp: int, in_out: str):
    last = db.query(Invoice).filter(Invoice.IDP == idp, Invoice.Over_Domestic == in_out).first()
    return last.IDOM

def get_last_rfi_number(db: Session, idp: int, idom: int, over_domestic: str):
    last = (db.query(TimeTable).filter(TimeTable.IDP == idp, TimeTable.IDOM == idom,
                                       TimeTable.Over_Domestic == over_domestic).order_by(
        TimeTable.RFI_Number.desc()).first())
    max_rfi = (
        db.query(func.max(TimeTable.RFI_Number))
        .filter(
            TimeTable.IDP == idp,
            TimeTable.IDOM == idom,
            TimeTable.Over_Domestic == over_domestic
        )
        .scalar()
    )
    if last and last.RFI_Number:
        return int(last.RFI_Number) + 1
    elif last and max_rfi:
        return int(max_rfi) + 1
    else:
        return 1
