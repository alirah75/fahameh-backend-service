from sqlalchemy import Column, Integer, String, Float, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database.models.base import Base


class Invoice(Base):
    __tablename__ = "T_Invoice"

    IDOM = Column("IDOM", Integer, primary_key=True)
    IDP = Column("IDP", Integer, primary_key=True)

    Over_Domestic = Column("Over-Domestic", String(100))
    UnitPrice = Column("UnitPrice", String(20))
    Price = Column("Price", Float)
    ProjectCode = Column("ProjectCode", String(100))

    __table_args__ = (
        PrimaryKeyConstraint("IDOM", "IDP"),
        ForeignKeyConstraint(["IDP"], ["T_Project.IDP"]),
    )

    project = relationship("Project", back_populates="invoices")
    timetables = relationship("TimeTable", back_populates="invoice")
    location_prices = relationship("Location_Price", back_populates="invoice")
