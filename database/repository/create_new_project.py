from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Invoice
from schemas.Project import ProjectCreate
from database.models.T_Project import Project


def insert_new_project(db: Session, data: ProjectCreate):
    last_id = db.query(func.max(Project.IDP)).scalar()
    new_project = Project(
        IDP=last_id+1,
        Title=data.Title
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    insert_new_invoice(db, last_id+1, data.project_code)

    return new_project


def insert_new_invoice(db: Session, idp, projectCode):
    IDOMS = [
        ("داخلی کالا", False),  # projectCode اصلی
        ("خارجی", True)  # projectCode با پسوند OS-
    ]

    for idom_text, is_os in IDOMS:
        last_idom = db.query(func.max(Invoice.IDOM)).scalar()
        # اگر خارجی باشد → پسوند OS اضافه شود
        if is_os:
            final_project_code = f"{projectCode}-OS"
        else:
            final_project_code = projectCode

        new_invoice = Invoice(
            IDP=idp,
            IDOM=last_idom + 1,
            Over_Domestic=idom_text,
            ProjectCode=final_project_code,
            Price=0
        )

        db.add(new_invoice)
        db.commit()