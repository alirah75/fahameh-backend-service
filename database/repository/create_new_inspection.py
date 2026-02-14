from sqlalchemy import text
from sqlalchemy.orm import Session
from database.models.T_RFIDate import RFI_Date
from schemas.TimeTable import AddInspectionDateSchema


def insert_new_rfi_date(db: Session, rfi_date: AddInspectionDateSchema):
    idrd = db.execute(text("""
        SELECT setval(
            't_rfidate_idrd_seq',
            (SELECT MAX("IDRD") FROM "T_RFIDate") + 1
        )
    """))


    new_rfi_date = RFI_Date(
        # IDRD = idrd,
        RFI_Numbering=rfi_date.RFI_Numbering,
        RFI_Date=rfi_date.RFI_Date,
        ApproveManday=rfi_date.ApproveManday,
        ApproveManday1=rfi_date.ApproveManday,
        Inspector_Name=rfi_date.Inspector_Name,
        InspectorPrice=rfi_date.InspectorPrice,
        FinalPrice=rfi_date.InspectorPrice,
        SubstituteInspector='0',
        SubstituteinspectorPrice='0',
    )

    db.add(new_rfi_date)
    db.commit()
    db.refresh(new_rfi_date)
    return new_rfi_date