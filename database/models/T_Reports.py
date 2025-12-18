from sqlalchemy import (
    Column, Integer, String, Float, Date, Text,
    ForeignKeyConstraint, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from database.models.base import Base


class Reports(Base):
    __tablename__ = "T_Reports"

    IDRE = Column("IDRE", Integer, primary_key=True, autoincrement=True)
    RFI_Numbering = Column("RFI_Numbering", String(100), primary_key=True)

    Report_No = Column("Report_No", String(100))
    RevNO = Column("RevNO", String(50))
    IssueDate = Column("IssueDate", Date)
    Doc_Status = Column("Doc_Status", String(50))
    Remark = Column("Remark", Text)
    App_manday_1stPrice = Column("App_manday_1stPrice", Float)
    FirstPrice = Column("1stPrice", Float)
    UnitNo = Column("UnitNo", String(50))
    VendorName = Column("VendorName", String(100))
    IRNNO = Column("IRNNO", String(100))
    SRNNO = Column("SRNNo", String(100))
    User = Column("User", String(100))
    ReportReceivedDate = Column("reportrecivedDatee", Date)
    DateShamsi = Column("DateShamsi", String(50))

    __table_args__ = (
        PrimaryKeyConstraint("IDRE", "RFI_Numbering"),

        # FK درست → اتصال به جدول T_TimeTable
        ForeignKeyConstraint(
            ["RFI_Numbering"],
            ["T_TimeTable.RFI_Numbering"]
        ),
    )

    # اتصال صحیح: Reports ⇐ TimeTable
    timetable = relationship("TimeTable", back_populates="reports")
