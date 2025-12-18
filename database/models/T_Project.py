from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models.base import Base


class Project(Base):
    __tablename__ = "T_Project"

    IDP = Column("IDP", Integer, primary_key=True, autoincrement=True)
    Title = Column("Title", String(255), unique=True)
    Abbreviation = Column("Abbreviation", String(255))
    SubProject = Column("SubProject", String(255))
    Material_Code = Column("Material_Code", String(255))
    Remark = Column("Remark", String(255))

    invoices = relationship("Invoice", back_populates="project")
