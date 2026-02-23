from typing import Optional

from sqlalchemy import distinct
from sqlalchemy.orm import Session
from schemas.Schema_Reports import ReportCreateSchema, ReportUpdateSchema
from database.models.T_Reports import Reports
from core.config import settings

def insert_new_report(db: Session, data: ReportCreateSchema):
    new_report = Reports(
            RFI_Numbering=data.rfi_numbering,
            Report_No=data.report_no,
            RevNO=data.rev_no,
            Doc_Status=data.Doc_Status,
            IssueDate=data.IssueDate,
            Remark=data.Remark,
            App_manday_1stPrice=data.App_manday_1stPrice,
            UnitNo=data.UnitNo,
            VendorName=data.VendorName,
            IRNNO=data.IRNNO,
            SRNNO=data.SRNNo,
            User=data.user,
            DateShamsi=settings.gregorian_to_jalali_str(data.IssueDate)
        )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


def find_report(db: Session, rfi_number: str, report_number=None):
    last = db.query(Reports).filter(
        Reports.RFI_Numbering == rfi_number,
        Reports.Report_No == report_number
    ).first()
    return last

def find_report_no(rfi_numbering, report_no, rev_no, db: Session):
    last_report = (
        db.query(Reports)
        .filter(
            Reports.RFI_Numbering == rfi_numbering,
            Reports.Report_No.like(f"{report_no}%")
            )
            .order_by(Reports.Report_No.desc())
            .first()
        )

    existing_no = last_report.Report_No if last_report else None

    new_report_no = generate_next_report_no(
        base_no=report_no,
        existing_no=existing_no,
        rev_type=rev_no
    )

    return {
        "base_report_no": report_no,
        "last_report_no": existing_no,
        "suggested_report_no": new_report_no
    }

def generate_next_report_no(base_no: str, existing_no: Optional[str], rev_type: str) -> str:
    """
    base_no: aa-vv-dd
    existing_no: aa-vv-dd / aa-vv-dd-1 / aa-vv-dd-A
    rev_type: rev | multi
    """

    if not existing_no or existing_no == base_no:
        if rev_type == "rev":
            return f"{base_no}-1"
        return f"{base_no}-A"

    suffix = existing_no.replace(base_no + "-", "")

    # عددی
    if suffix.isdigit():
        return f"{base_no}-{int(suffix) + 1}"

    # حرفی
    if suffix.isalpha():
        return f"{base_no}-{next_alpha(suffix)}"

    # fallback
    return f"{base_no}-1"


def next_alpha(s: str) -> str:
    s = s.upper()
    carry = 1
    result = []

    for c in reversed(s):
        if carry == 0:
            result.append(c)
            continue

        if c == 'Z':
            result.append('A')
            carry = 1
        else:
            result.append(chr(ord(c) + 1))
            carry = 0

    if carry:
        result.append('A')

    return ''.join(reversed(result))

def get_all_report_statuses(db: Session):
    return (db.query(distinct(Reports.Doc_Status))
        .filter(
            Reports.Doc_Status.isnot(None),
            Reports.Doc_Status.notin_(['', 'string'])
        )
        .order_by(Reports.Doc_Status.asc())
        .all()
    )

def update_report(db: Session, rfi_number: str, data: ReportUpdateSchema):
    obj = db.query(Reports)\
        .filter(Reports.RFI_Numbering == rfi_number)\
        .first()

    if not obj:
        return None

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)

    return obj
