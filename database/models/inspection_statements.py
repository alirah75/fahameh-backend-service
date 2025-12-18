from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship
from database.models.base import Base
from database.models.inspection import Inspection


class InspectionStatement(Base):
    __tablename__ = "inspection_statements"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)

    inspection_date = Column(Date, nullable=True)        # YYYY-MM-DD
    approval_status = Column(String(100), nullable=True)
    inspector_name = Column(String(200), nullable=False)
    fee = Column(Float, nullable=True)

    second_inspector_name = Column(String(200), nullable=True)
    second_inspector_fee = Column(Float, nullable=True)

    remark = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="statements")

    def __repr__(self):
        return f"<InspectionStatement(id={self.id}, date={self.inspection_date})>"