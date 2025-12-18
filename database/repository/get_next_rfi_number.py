from sqlalchemy.orm import Session
from database.models.T_Invoice import Invoice
from database.models.T_TimeTable import TimeTable


def get_full_rfi_info(db: Session, idp, in_out: str, over_domestic):
    idom = find_idom_value(db, idp, in_out)
    next_rfi = get_last_rfi_number(db, idp, idom, in_out)
    return idom, next_rfi


def find_idom_value(db: Session, idp: int, in_out: str):
    last = db.query(Invoice).filter(Invoice.IDP == idp, Invoice.Over_Domestic == in_out).first()
    return last.IDOM

def get_last_rfi_number(db: Session, idp: int, idom: int, over_domestic: str):
    if over_domestic == 'داخلی کالا':
        last = (db.query(TimeTable).filter(TimeTable.IDP == idp, TimeTable.IDOM == idom).order_by(
            TimeTable.RFI_Number.desc()).first())
    elif over_domestic == 'خارجی':
        last = (db.query(TimeTable).filter(TimeTable.IDP == idp, TimeTable.IDOM == idom,
                                           TimeTable.Over_Domestic == over_domestic).order_by(
            TimeTable.RFI_Number.desc()).first())
    if last and last.RFI_Number:
        return int(last.RFI_Number) + 1
    else:
        return 1
