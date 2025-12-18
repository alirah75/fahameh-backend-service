from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Permit(Base):
    __tablename__ = "permit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    permit = Column(String(50), nullable=False)
    unit = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Permit user_name={self.user_name} permit={self.permit} unit={self.unit}>"
