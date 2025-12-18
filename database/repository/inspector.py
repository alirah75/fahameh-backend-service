from sqlalchemy.orm import Session
from database.models.T_Inspector import Inspector

def get_all_inspectors(db: Session):
    return db.query(Inspector).order_by(Inspector.Inspector_Name.asc()).all()

def get_inspector_by_id(db: Session, id_ins: int):
    return db.query(Inspector).filter(Inspector.ID_Ins == id_ins).first()
