from sqlalchemy.orm import Session
from database.models.T_Inspector import Inspector
from schemas.Schema_Inspectors import InspectorCreateSchema, InspectorUpdateSchema


def get_all_inspectors(db: Session):
    return db.query(Inspector).order_by(Inspector.Inspector_Name.asc()).all()

def get_inspector_by_id(db: Session, id_ins: int):
    return db.query(Inspector).filter(Inspector.ID_Ins == id_ins).first()

def create_inspector(db: Session, data: InspectorCreateSchema):
    new_inspector = Inspector(**data.dict())
    db.add(new_inspector)
    db.commit()
    db.refresh(new_inspector)
    return new_inspector

def update_inspector(db: Session, inspector: Inspector, data: InspectorUpdateSchema):
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inspector, key, value)
    db.commit()
    db.refresh(inspector)
    return inspector

def delete_inspector(db: Session, inspector: Inspector):
    db.delete(inspector)
    db.commit()
