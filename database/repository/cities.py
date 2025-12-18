from sqlalchemy.orm import Session
from database.models.city import City

def get_cities_by_province(db: Session, province_id: int):
    return db.query(City).filter(City.province_id == province_id).order_by(City.name).all()
