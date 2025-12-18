from sqlalchemy import Column, String
from database.models.base import Base


class User(Base):
    __tablename__ = "User"

    user_name = Column("User_Name", String(255), primary_key=True)
    password = Column("Password", String(255))
    permit = Column("Permit",String(255))
    unit = Column("Unit",String(255))
