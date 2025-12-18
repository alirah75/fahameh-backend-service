from sqlalchemy import Column, Integer, String, Float, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database.models.base import Base


class DateMonthsName(Base):
    __tablename__ = "S_DateMonthsName"

    IdMonth = Column("IdMonth", Integer, primary_key=True)
    HejriFarsi = Column("HejriFarsi", String(50))
    HejriEnglish = Column("HejriEnglish", String(50))
    MiladiFarsi = Column("MiladiFarsi", String(50))
    MiladiEnglish = Column("MiladiEnglish", String(50))

    dates = relationship("S_Date", back_populates="month")

