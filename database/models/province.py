from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.models.base import Base
from database.models.city import City


class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    cities = relationship("City", back_populates="province", cascade="all, delete")

    def __repr__(self):
        return f"<Province(id={self.id}, name='{self.name}')>"