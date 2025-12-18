from sqlalchemy import Column, Integer, String, Float, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database.models.base import Base

class Location_Price(Base):
    __tablename__ = "T_Location_Price"

    ID = Column("ID", Integer, primary_key=True)
    IDP = Column("IDP", Integer, primary_key=True)
    IDOM = Column("IDOM", Integer, primary_key=True)

    Overlocation = Column("Overlocation", String(200))
    location = Column("location", String(200))
    OverDome = Column("OverDome", String(50))
    Price = Column("Price", Float)
    UnitPrice = Column("UnitPrice", Float)

    __table_args__ = (
        PrimaryKeyConstraint("ID", "IDP", "IDOM"),
        ForeignKeyConstraint(["IDP", "IDOM"],
                             ["T_Invoice.IDP", "T_Invoice.IDOM"]),
    )

    invoice = relationship("Invoice", back_populates="location_prices")
