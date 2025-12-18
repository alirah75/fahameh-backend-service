from sqlalchemy import (
    Column, Integer, String, Float, Date,
    ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from database.models.base import Base


class RFI_Date(Base):
    __tablename__ = "T_RFIDate"

    # ✅ کلید اصلی
    IDRD = Column("IDRD", Integer, primary_key=True, autoincrement=True)

    # ستون‌ها
    RFI_Date = Column("RFI_Date", Date)
    Inspector_Name = Column("Inspector_Name", String(100))
    InspectorPrice = Column("InspectorPrice", Float)

    ApproveManday = Column("Approvemanday", String(100))
    SubstituteInspector = Column("Substituteinspector", String(100))
    SubstituteinspectorPrice = Column("SubstituteinspectorPrice", String(100))

    FinalPrice = Column("FinalPrice", Float)
    ApproveManday1 = Column("Approvemanday1", String(100))

    # ❗ دیگر کلید اصلی نیست
    RFI_Numbering = Column(
        String(100),
        ForeignKey("T_TimeTable.RFI_Numbering", ondelete="CASCADE"),
        nullable=False
    )

    # رابطه
    timetable = relationship("TimeTable", back_populates="rfidates")
