from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status

from database.models.token_blacklist import TokenBlacklist
# from database.repository.user import get_all_users
from database.session import get_db
from routers.route_login import get_current_user
from schemas.user import UserBase

router = APIRouter()

@router.get("/users/me")
def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return [current_user.user_name, current_user.permit]


@router.post("/user/logout", status_code=status.HTTP_200_OK)
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