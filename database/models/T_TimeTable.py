from sqlalchemy import (
    Column, Integer, String, Date,
    ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database.models.base import Base


class TimeTable(Base):
    __tablename__ = "T_TimeTable"

    IDP = Column("IDP", Integer)
    IDOM = Column("IDOM", Integer)
    IDR = Column("IDR", Integer)

    RFI_Numbering = Column("RFI_Numbering", String(100), unique=True)

    InspectionDate = Column("InspectionDate", Date)
    Over_Domestic = Column("Over_Domestic", String(100))
    InspectionLocation = Column("InspectionLocation", String(200))
    RFI_Number = Column("RFI_Number", Integer)
    RFI_Recived_Date = Column("RFI_Recived_Date", Date)
    RFI_Status = Column("RFI_Status", String(100))
    VendorName = Column("VendorName", String(100))
    Inspection_Duration = Column("Inspection_Duration", Integer)
    Inspector_Name = Column("Inspector_Name", String(100))
    Remark = Column("Remark", String(200))
    QTY_3rdpartinspector = Column("QTY-3rdpartinspector", String(100))
    approved_Duration = Column("approved-Duration", String(100))
    Material = Column("Material", String(100))
    User_Name = Column("User_Name", String(100))
    FolderNo = Column("FolderNo", Integer)
    NotificationNo = Column("NotificationNo", String(100))
    DateShamsi = Column("DateShamsi", String(50))
    Inspector_Type = Column("Inspector_Type", String(50))
    Goods_Description = Column("Goods_Description", String(200))

    __table_args__ = (
        PrimaryKeyConstraint("IDP", "IDOM", "IDR"),

        UniqueConstraint("IDR", "RFI_Numbering"),

        # درست و بدون خطا
        ForeignKeyConstraint(
            ["IDP", "IDOM"],
            ["T_Invoice.IDP", "T_Invoice.IDOM"]
        ),
    )

    invoice = relationship("Invoice", back_populates="timetables")
    rfidates = relationship("RFI_Date", back_populates="timetable")
    reports = relationship("Reports", back_populates="timetable")
