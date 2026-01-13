from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# اطلاعات پروژه
class ProjectInfoSchema(BaseModel):
    projectName: str
    province: str
    city: str
    vendor: str


# اطلاعات بازرس
class InspectorInfoSchema(BaseModel):
    inspectorName: str
    inspectorLocation: str
    phoneNumber: str
    email: str
    expertise: str
    fee: float


# نوتیفیکیشن‌ها
class InspectionDateSchema(BaseModel):
    startDate: date
    endDate: date


class NotificationSchema(BaseModel):
    registrationNumber: str
    sendDate: date
    inspectionDaysCount: int
    inspectionDate: InspectionDateSchema


# گزارش‌ها
class ReportSchema(BaseModel):
    reportNumber: str
    receiveDate: date
    status: str


# صورتجلسه‌های بازرسی
class InspectionStatementSchema(BaseModel):
    inspectionDate: date
    approvalStatus: str
    inspectorName: str
    fee: float
    secondInspectorName: Optional[str] = None
    secondInspectorFee: Optional[float] = None


# مدل اصلی درخواست (Request Body)
class InspectionCreateSchema(BaseModel):
    projectInfo: ProjectInfoSchema
    inspectorInfo: InspectorInfoSchema
    notifications: List[NotificationSchema]
    reports: List[ReportSchema]
    inspectionStatements: List[InspectionStatementSchema]
