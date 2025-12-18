# database/models/inspection.py
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from database.models.base import Base


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)

    # اطلاعات پروژه
    project_name = Column(String(255), nullable=False)
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    vendor = Column(String(255), nullable=True)

    # اطلاعات بازرس
    inspector_name = Column(String(200), nullable=False)
    inspector_location = Column(String(200), nullable=True)
    phone_number = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    expertise = Column(String(200), nullable=True)
    fee = Column(Float, nullable=True)

    # اطلاعات سیستم
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # رابطه‌ها (در آینده در صورت وجود Notification, Report, Statement)
    notifications = relationship(
        "Notification",
        back_populates="inspection",
        cascade="all, delete-orphan",        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Inspection(id={self.id}, project='{self.project_name}', inspector='{self.inspector_name}')>"
