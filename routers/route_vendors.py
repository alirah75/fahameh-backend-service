from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.session import get_db

from database.models.vendor import Vendor
from database.repository.get_vendors import fetch_vendors_name
from database.repository.create_new_vendor import insert_new_vendor
from routers.route_login import get_current_user

from schemas.Vendor import VendorCreate


router = APIRouter()


@router.get("/{project_type}", summary="دریافت لیست تمام وندورها")
def list_vendors(project_type, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vendors = fetch_vendors_name(db, project_type)

    if not vendors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ وندوری یافت نشد"
        )

    vendor_names = {i: vendor[0] for i, vendor in enumerate(vendors, start=1)}

    return vendor_names


@router.post('/')
def create_new_vendor(data: VendorCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Vendor).filter(Vendor.name == data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Vendor Name "{data.name}" already exists.'
        )
    new_item = insert_new_vendor(db, data)
    return {"message": "Created new vendor successfully", "data": new_item.id}