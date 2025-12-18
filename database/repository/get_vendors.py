from sqlalchemy.orm import Session
from sqlalchemy import distinct
# from database.models.T_Reports import Reports
from database.models.vendor import Vendor


def fetch_vendors_name(db: Session, project_type):
    return (
        db.query(distinct(Vendor.name))
        .filter(Vendor.over_domestic == project_type)
        .order_by(Vendor.name.asc())
        .all()
    )
