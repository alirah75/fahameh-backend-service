import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.session import get_db
from database.db import engine
from database.models.base import Base
from apis.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.title, description=settings.description, version=settings.version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    create_tables()
    include_router(app)
    return app


app = start_application()


@app.get('/')
def home():
    return RedirectResponse(url='http://localhost:5173/login', status_code=status.HTTP_307_TEMPORARY_REDIRECT)



@app.get("/health/db")
def health_check_db() -> Dict[str, str]:
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8001, reload=True)
