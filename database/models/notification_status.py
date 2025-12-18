from sqlalchemy import Column, Integer, String
from database.models.base import Base

class NotificationStatus(Base):
    __tablename__ = "notification_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)