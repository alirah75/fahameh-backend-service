from sqlalchemy.orm import Session
from database.models.T_Location import Location


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