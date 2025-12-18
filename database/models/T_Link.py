from sqlalchemy import Column, Integer, String
from database.models.base import Base


class Link(Base):
    __tablename__ = "T-Link"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Report_No = Column("Report_No", String)
    Folder_Path = Column("Folder_Path", String)
