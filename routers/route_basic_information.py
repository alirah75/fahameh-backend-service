from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.repository.get_daily_report import daily_report
from database.session import get_db
from routers.route_login import get_current_user


router = APIRouter()



