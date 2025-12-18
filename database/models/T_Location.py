from sqlalchemy import Column, Integer, String, Numeric
from database.models.base import Base


class Location(Base):
    __tablename__ = "T_Location"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Overlocation = Column("Overlocation", String)
    location = Column("location", String)
    OverDome = Column("OverDome", String)
    Price = Column("Price", Numeric(10, 2))
    UnitPrice = Column("UnitPrice", String)
