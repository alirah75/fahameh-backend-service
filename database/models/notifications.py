# database/models/notifications.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models.inspection import Inspection


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)

    registration_number = Column(String(100), nullable=False)
    send_date = Column(Date, nullable=True)
    inspection_days_count = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    note = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, reg='{self.registration_number}')>"
