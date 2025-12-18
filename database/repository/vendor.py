from sqlalchemy.orm import Session
from sqlalchemy import distinct
# from database.models.T_Reports import Reports
from database.models.vendor import Vendor


def get_vendors_name(db: Session):
    return db.query(distinct(Vendor.name)).order_by(Vendor.name.asc()).all()
