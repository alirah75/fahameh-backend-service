from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from database.session import get_db
from database.repository.in_out import get_inout_list
from routers.route_login import get_current_user

router = APIRouter()

@router.get("/", summary="دریافت لیست مقدارهای غیرتکراری Cmbinout از جدول T_Invoice", status_code=status.HTTP_200_OK)
def list_inout(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    values = get_inout_list(db, column_name="Over_Domestic")

    if not values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ مقداری یافت نشد"
        )

    return {i: val for i, val in enumerate(values)}
