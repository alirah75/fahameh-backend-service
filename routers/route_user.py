from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database.models.token_blacklist import TokenBlacklist
from database.repository import user_crud
from database.session import get_db
from routers.route_login import get_current_user
from schemas.Schema_User import UserBaseSchema, UserCreateSchema, UserUpdate

router = APIRouter()

@router.get("/me", status_code=status.HTTP_200_OK)
def read_users_me(current_user: UserBaseSchema = Depends(get_current_user)):
    return [current_user.user_name, current_user.permit]


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # استخراج توکن از هدر
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]

    # ذخیره در blacklist
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    db.commit()

    return {"message": "Logout successful"}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing_user = user_crud.get_user_by_username(db, user.user_name)

    if existing_user:
        raise HTTPException(status_code=400, detail="کاربر قبلاً وجود دارد")

    user_crud.create_user(db, user)
    return {"message": "کاربر با موفقیت ایجاد شد"}


@router.put("/{user_name}")
def update_user(user_name: str, user_data: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = user_crud.get_user_by_username(db, user_name)

    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")

    user_crud.update_user(db, user, user_data)
    return {"message": "اطلاعات کاربر بروزرسانی شد"}


@router.delete("/{user_name}")
def delete_user(user_name: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = user_crud.get_user_by_username(db, user_name)

    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")

    user_crud.delete_user(db, user)
    return {"message": "کاربر حذف شد"}
