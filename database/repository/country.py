from sqlalchemy.orm import Session
from database.models.country import Country

def get_countries(db: Session):
    provinces = db.query(Country).order_by(Country.title.asc()).all()
    return provinces