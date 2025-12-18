from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models.base import Base

class DateDaysNam(Base):
    __tablename__ = "S_DateDaysNam"

    IdRooz = Column("IdRooz", Integer, primary_key=True)
    RoozShamsi = Column("RoozShamsi", String(50))
    RoozMiladi = Column("RoozMiladi", String(50))

    dates = relationship("S_Date", back_populates="day")
