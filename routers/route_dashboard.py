from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database.session import get_db
from routers.route_login import get_current_user

router = APIRouter()

# @router.get('/dashboard')
# def dashboard(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     return {
#         "message": f"Welcome to your dashboard, {current_user} 👋",
#         "status": "Access granted",
#     }
