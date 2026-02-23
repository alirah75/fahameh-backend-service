from sqlalchemy.orm import Session
from sqlalchemy import distinct
# from database.models.T_Reports import Reports
from database.models.vendor import Vendor
from schemas.Schema_Vendor import VendorCreate, VendorUpdate


def get_all_vendors(db: Session, project_type):
    return (
        db.query(distinct(Vendor.name))
        .filter(Vendor.over_domestic == project_type)
        .order_by(Vendor.name.asc())
        .all()
    )

def get_vendor_by_id(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def create_vendor(db: Session, data: VendorCreate):
    new_vendor = Vendor(**data.dict())
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor


def update_vendor(db: Session, vendor: Vendor, data: VendorUpdate):
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vendor, key, value)

    db.commit()
    db.refresh(vendor)
    return vendor


def delete_vendor(db: Session, vendor: Vendor):
    db.delete(vendor)
    db.commit()
