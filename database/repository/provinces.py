from sqlalchemy.orm import Session
from database.models.province import Province

def get_provinces(db: Session):
    provinces = db.query(Province).order_by(Province.name.asc()).all()
    return provinces