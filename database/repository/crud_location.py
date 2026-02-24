from sqlalchemy.orm import Session
from database.models.T_Location import Location
from database.models.country import Country
from schemas.Schema_Country import CountryCreate, CountryUpdate


def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.ID == location_id).first()


def get_all_locations(db: Session):
    return db.query(Location).all()


def create_location(db: Session, location_data):
    new_location = Location(**location_data.dict())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def update_location(db: Session, db_location: Location, location_data):
    update_data = location_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location


def delete_location(db: Session, db_location: Location):
    db.delete(db_location)
    db.commit()


def get_countries(db: Session):
    country = db.query(Country).order_by(Country.title.asc()).all()
    return country


def get_country_by_id(db: Session, country_id: int):
    return db.query(Country).filter(Country.id == country_id).first()

def create_country(db: Session, data: CountryCreate):
    new_country = Country(**data.dict())
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


def update_country(db: Session, country: Country, data: CountryUpdate):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(country, key, value)

    db.commit()
    db.refresh(country)
    return country


def delete_country(db: Session, country: Country):
    db.delete(country)
    db.commit()
