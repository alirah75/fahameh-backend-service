from sqlalchemy.orm import Session

from schemas.Vendor import VendorCreate
from database.models.vendor import Vendor

def insert_new_vendor(db: Session, data: VendorCreate):
    new_vendor = Vendor(
        name=data.name,
        over_domestic=data.over_domestic
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor
