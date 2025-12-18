from sqlalchemy import Column, Integer, String, Numeric
from database.models.base import Base


class Inspector(Base):
    __tablename__ = "T_Inspector"

    ID_Ins = Column("ID_Ins", Integer, primary_key=True, autoincrement=True)
    Inspector_Name = Column("Inspector_Name", String(255))
    PersonnelCode = Column("PersonnelCode", String(255))
    Inspector_Discipline = Column("Inspector_Discipline", String(255))
    Inspector_Email = Column("Inspector_Email", String(255))
    Inspector_phone_no = Column("Inspector_phone_no", String(255))
    Location_Coverd = Column("Location_Coverd", String(255))
    status = Column("status", String(50))
    Price = Column("Price", Numeric(18, 2))
    OVRDom = Column("OVRDom", String(255))
    Price1403 = Column("Price1403", Numeric(18, 2))
