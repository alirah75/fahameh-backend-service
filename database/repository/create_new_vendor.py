from sqlalchemy.orm import Session

from schemas.Vendor import VendorCreateSchema
from database.models.vendor import Vendor

def insert_new_vendor(db: Session, data: VendorCreateSchema):
    new_vendor = Vendor(
        name=data.name,
        over_domestic=data.over_domestic
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor
