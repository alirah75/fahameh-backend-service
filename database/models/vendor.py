from sqlalchemy import Column, Integer, String, Boolean
from database.models.base import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    contact_person = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    over_domestic = Column("Over-Domestic", Boolean)

    def __repr__(self):
        return f"<Vendor(id={self.id}, name='{self.name}')>"
