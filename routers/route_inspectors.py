from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from database.repository.inspector import get_all_inspectors, get_inspector_by_id
from database.session import get_db
from routers.route_login import get_current_user


router = APIRouter()

@router.get("/", summary="دریافت لیست تمام بازرسان‌ها", status_code=status.HTTP_200_OK)
def list_inspectors(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    inspectors = get_all_inspectors(db)

    if not inspectors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ بازرس فعالی یافت نشد"
        )

    return {inspector.ID_Ins: inspector.Inspector_Name for inspector in inspectors}


@router.get("/{inspector_id}", summary="دریافت مشخصات یک بازرس", status_code=status.HTTP_200_OK)
def get_inspector(inspector_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    inspector = get_inspector_by_id(db, inspector_id)

    if not inspector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بازرس مورد نظر یافت نشد"
        )

    return {
        "Inspector_Name": inspector.Inspector_Name,
        "PersonnelCode": inspector.PersonnelCode,
        "Inspector_Email": inspector.Inspector_Email,
        "Inspector_phone_no": inspector.Inspector_phone_no,
        "Location_Coverd": inspector.Location_Coverd,
        "status": inspector.status,
        "Price": inspector.Price,
    }