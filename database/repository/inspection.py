from sqlalchemy.orm import Session
from database.models.inspection import Inspection
from schemas.inspection import InspectionCreate

def create_inspection(db: Session, inspection_data: InspectionCreate):
    new_inspection = Inspection(
        project_name=inspection_data.projectInfo.projectName,
        province=inspection_data.projectInfo.province,
        city=inspection_data.projectInfo.city,
        vendor=inspection_data.projectInfo.vendor,
        inspector_name=inspection_data.inspectorInfo.inspectorName,
        inspector_location=inspection_data.inspectorInfo.inspectorLocation,
        phone_number=inspection_data.inspectorInfo.phoneNumber,
        email=inspection_data.inspectorInfo.email,
        expertise=inspection_data.inspectorInfo.expertise,
        fee=inspection_data.inspectorInfo.fee,
    )
    db.add(new_inspection)
    db.commit()
    db.refresh(new_inspection)
    return new_inspection
