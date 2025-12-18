from fastapi import APIRouter

from routers import route_user
from routers import route_login
from routers import route_dashboard
from routers import route_lookups
from routers import route_locations
from routers import route_inspectors
from routers import route_projects
from routers import route_vendors
from routers import route_reports
from routers import route_notifications


api_router = APIRouter()
api_router.include_router(route_notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(route_inspectors.router, prefix="/inspectors", tags=["inspectors"])
api_router.include_router(route_locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(route_projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(route_vendors.router, prefix="/vendors", tags=["vendors"])
api_router.include_router(route_reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(route_lookups.router, prefix="/lookups", tags=["lookups"])
api_router.include_router(route_dashboard.router, prefix="", tags=["dashboard"])
api_router.include_router(route_login.router, prefix="", tags=["login"])
api_router.include_router(route_user.router,prefix="",tags=["users"])
