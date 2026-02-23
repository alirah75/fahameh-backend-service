from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.session import get_db

from database.models.vendor import Vendor
from database.repository.crud_vendors import get_all_vendors, get_vendor_by_id, create_vendor, update_vendor, \
    delete_vendor
# from database.repository.create_new_vendor import insert_new_vendor
from routers.route_login import get_current_user

from schemas.Schema_Vendor import VendorCreate, VendorRead, VendorUpdate

router = APIRouter()


@router.get("/", summary="دریافت لیست تمام وندورها", status_code=status.HTTP_200_OK)
def list_vendors(project_type: bool, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vendors = get_all_vendors(db, project_type)
    if not vendors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ وندوری یافت نشد"
        )

    vendor_names = {i: vendor[0] for i, vendor in enumerate(vendors, start=1)}

    return vendor_names


@router.get("/{vendor_id}", response_model=VendorRead)
def get_vendor(vendor_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vendor = get_vendor_by_id(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="فروشنده یافت نشد")
    return vendor


@router.post("/", response_model=VendorRead, status_code=status.HTTP_201_CREATED)
def add_vendor(data: VendorCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Vendor).filter(Vendor.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="این فروشنده قبلاً ثبت شده است")

    return create_vendor(db, data)

@router.put("/{vendor_id}", response_model=VendorRead)
def edit_vendor(vendor_id: int, data: VendorUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vendor = get_vendor_by_id(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="فروشنده یافت نشد")

    return update_vendor(db, vendor, data)
@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_vendor(vendor_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vendor = get_vendor_by_id(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="فروشنده یافت نشد")

    delete_vendor(db, vendor)
