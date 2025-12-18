from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database.models.base import Base
# from database.models.inspection import Inspection


class Report(Base):
    __tablename__ = "inspection_reports"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)

    report_number = Column(String(100), nullable=False)
    receive_date = Column(Date, nullable=True)   # YYYY-MM-DD
    status = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, report_number='{self.report_number}')>"