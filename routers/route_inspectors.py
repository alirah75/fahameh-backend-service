from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from database.repository.crud_inspector import get_all_inspectors, get_inspector_by_id, delete_inspector, \
    update_inspector, create_inspector
from database.session import get_db
from routers.route_login import get_current_user
from schemas.Schema_Inspectors import InspectorReadSchema, InspectorUpdateSchema, InspectorCreateSchema

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


@router.get("/{inspector_id}",
            summary="دریافت مشخصات یک بازرس",
            response_model=InspectorReadSchema,
            status_code=status.HTTP_200_OK
            )
def get_inspector(
    inspector_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inspector = get_inspector_by_id(db, inspector_id)

    if not inspector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بازرس مورد نظر یافت نشد"
        )

    return inspector


@router.post("/", response_model=InspectorReadSchema, status_code=status.HTTP_201_CREATED)
def add_inspector(data: InspectorCreateSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_inspector(db, data)

@router.put("/{inspector_id}", response_model=InspectorReadSchema)
def edit_inspector(inspector_id: int, data: InspectorUpdateSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    inspector = get_inspector_by_id(db, inspector_id)
    if not inspector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بازرس یافت نشد")
    return update_inspector(db, inspector, data)

@router.delete("/{inspector_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_inspector(inspector_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    inspector = get_inspector_by_id(db, inspector_id)
    if not inspector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بازرس یافت نشد")
    delete_inspector(db, inspector)
