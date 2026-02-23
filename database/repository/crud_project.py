from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Invoice
from database.models.T_Project import Project
from schemas.Schema_Project import ProjectCreate


def get_all_projects(db: Session):
    return db.query(Project).order_by(Project.Title.asc()).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.IDP == project_id).first()


def create_new_project(db: Session, data: ProjectCreate):
    last_id = db.query(func.max(Project.IDP)).scalar()
    new_project = Project(
        IDP=last_id+1,
        Title=data.Title
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    create_new_invoice(db, last_id+1, data.project_code)

    return new_project


def create_new_invoice(db: Session, idp, projectCode):
    IDOMS = [
        ("داخلی کالا", False),
        ("خارجی", True)
    ]

    for idom_text, is_os in IDOMS:
        last_idom = db.query(func.max(Invoice.IDOM)).scalar()

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


def update_existing_project(db: Session, db_project: Project, data):
    if data.Title is not None:
        db_project.Title = data.Title

    if hasattr(data, "Abbreviation") and data.Abbreviation is not None:
        db_project.Abbreviation = data.Abbreviation

    if hasattr(data, "SubProject") and data.SubProject is not None:
        db_project.SubProject = data.SubProject

    if hasattr(data, "Material_Code") and data.Material_Code is not None:
        db_project.Material_Code = data.Material_Code

    if hasattr(data, "Remark") and data.Remark is not None:
        db_project.Remark = data.Remark

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_existing_project(db: Session, db_project: Project):
    db.query(Invoice).filter(Invoice.IDP == db_project.IDP).delete()

    db.delete(db_project)
    db.commit()
