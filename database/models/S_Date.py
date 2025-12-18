from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base


class S_Date(Base):
    __tablename__ = "S_Date"

    id = Column(Integer, primary_key=True, autoincrement=True)

    DateMiladi = Column(Date)
    DateShamsi = Column(String(20))

    IdMonthShamsi = Column(Integer)
    IdMonthMiladi = Column(Integer, ForeignKey("S_DateMonthsName.IdMonth"))
    IdDay = Column(Integer, ForeignKey("S_DateDaysNam.IdRooz"))

    # روابط
    day = relationship("DateDaysNam", back_populates="dates")
    month = relationship("DateMonthsName", back_populates="dates")

