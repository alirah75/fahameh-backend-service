from sqlalchemy import create_engine
from core.config import settings


print(f"DATABASE_URL is: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL)