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
from routers import route_pdf_reports
from routers import route_manager


api_router = APIRouter()
api_router.include_router(route_notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(route_projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(route_reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(route_pdf_reports.router, prefix="/pdf_reports", tags=["Pdf_Reports"])
api_router.include_router(route_locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(route_vendors.router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(route_inspectors.router, prefix="/inspectors", tags=["Inspectors"])
api_router.include_router(route_lookups.router, prefix="/lookups", tags=["Lookups"])
api_router.include_router(route_dashboard.router, prefix="", tags=["Dashboard"])
api_router.include_router(route_login.router, prefix="", tags=["Login"])
api_router.include_router(route_user.router,prefix="/users",tags=["Users"])
api_router.include_router(route_manager.router,prefix="/manager",tags=["Manager"])
