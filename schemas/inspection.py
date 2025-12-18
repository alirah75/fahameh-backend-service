from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# اطلاعات پروژه
class ProjectInfo(BaseModel):
    projectName: str
    province: str
    city: str
    vendor: str


# اطلاعات بازرس
class InspectorInfo(BaseModel):
    inspectorName: str
    inspectorLocation: str
    phoneNumber: str
    email: str
    expertise: str
    fee: float


# نوتیفیکیشن‌ها
class InspectionDate(BaseModel):
    startDate: date
    endDate: date


class Notification(BaseModel):
    registrationNumber: str
    sendDate: date
    inspectionDaysCount: int
    inspectionDate: InspectionDate


# گزارش‌ها
class Report(BaseModel):
    reportNumber: str
    receiveDate: date
    status: str


# صورتجلسه‌های بازرسی
class InspectionStatement(BaseModel):
    inspectionDate: date
    approvalStatus: str
    inspectorName: str
    fee: float
    secondInspectorName: Optional[str] = None
    secondInspectorFee: Optional[float] = None


# مدل اصلی درخواست (Request Body)
class InspectionCreate(BaseModel):
    projectInfo: ProjectInfo
    inspectorInfo: InspectorInfo
    notifications: List[Notification]
    reports: List[Report]
    inspectionStatements: List[InspectionStatement]
