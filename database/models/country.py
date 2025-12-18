from sqlalchemy import Column, String, Integer
from database.models.base import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String(4), nullable=False)
    title = Column(String(20), nullable=False)


    def __repr__(self):
        return f"<Country(id={self.id}, summary='{self.summary}', title='{self.title}')>"
