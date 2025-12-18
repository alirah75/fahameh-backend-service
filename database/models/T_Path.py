from sqlalchemy import Column, Integer, String
from database.models.base import Base


class Path(Base):
    __tablename__ = "T_Path"

    IDPath = Column("IDPath",Integer, primary_key=True, autoincrement=True)
    IDV = Column("IDV",Integer)
    Vendor = Column("Vendor",String)
    Path = Column("Path",String)
    Remark = Column("Remark",String)
    Material = Column("Material",String)
    MateialCode = Column("Mateial-Code",String)
