from sqlalchemy.orm import Session
from enum import Enum
from fastapi import Depends, APIRouter, HTTPException, status, Query
from database.repository.create_new_report import insert_new_report
from database.repository.get_report_no import find_report_no
from database.repository.report_service import update_report_fields, commit_report_update, get_report_by_rfi, \
    delete_report_commit, get_report_by_report_number
from database.session import get_db

from database.repository.get_one_report import find_report
from database.repository.get_rfi_report import get_report_rfi
from routers.route_login import get_current_user
from schemas.Reports import ReportCreateSchema, ReportUpdateSchema

router = APIRouter()

class RevType(str, Enum):
    rev = "rev"
    multipart = "multipart"

# @router.get("/rfi/", status_code=status.HTTP_200_OK)
# def fetch_rfi_report(project_name, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     data = get_report_rfi(project_name, db)
#     if not data:
#         return []
#
#     result = {}
#     for i, (
#             rfi_number,
#             rfi_status,
#             inspection_date,
#             report_no,
#             irnno,
#             App_manday_1stPrice,
#             NotificationNo,
#             RFI_Numbering,
#             title,
#             over_domestic,
#             vendor_name
#     ) in enumerate(data, start=1):
#         result[str(i)] = {
#             "RFI_Number": rfi_number,
#             "RFI_Status": rfi_status,
#             "InspectionDate": inspection_date,
#             "Report_No": report_no,
#             "IRNNO": irnno,
#             "Duration": App_manday_1stPrice,
#             "NotificationNo": NotificationNo,    # ToDo change RFI_Numbering with NotificationNo in ui
#             "RFI_Numbering": RFI_Numbering,    # ToDo change RFI_Numbering with NotificationNo in ui
#             "ProjectTitle": title,
#             "Over_Domestic": over_domestic,
#             "VendorName": vendor_name
#         }
#
#     return result

@router.get("/rfi/", status_code=status.HTTP_200_OK)
def fetch_rfi_report(project_name, project_type=str(1), current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if project_type == '0':
        project_type = 'خارجی'
    elif project_type == '1':
        project_type = 'داخلی کالا'
    elif project_type == '2':
        project_type = 'داخلی کشتی'
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='project type is not correct')


    data = get_report_rfi(project_name, project_type, db)
    if not data:
        return []

    result = {}
    for i, (
            rfi_number,
            rfi_status,
            inspection_date,
            report_no,
            irnno,
            App_manday_1stPrice,
            NotificationNo,
            RFI_Numbering,
            title,
            over_domestic,
            vendor_name
    ) in enumerate(data, start=1):
        result[str(i)] = {
            "RFI_Number": rfi_number,
            "RFI_Status": rfi_status,
            "InspectionDate": inspection_date,
            "Report_No": report_no,
            "IRNNO": irnno,
            "Duration": App_manday_1stPrice,
            "NotificationNo": NotificationNo,    # ToDo change RFI_Numbering with NotificationNo in ui
            "RFI_Numbering": RFI_Numbering,    # ToDo change RFI_Numbering with NotificationNo in ui
            "ProjectTitle": title,
            "Over_Domestic": over_domestic,
            "VendorName": vendor_name
        }

    return result


@router.get('/{rfi_number}', summary='نمایش اطلاعات یک گزارش', status_code=status.HTTP_200_OK)
def retrieve_one_report(rfi_number, report_number, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    report = find_report(db=db, rfi_number=rfi_number, report_number=report_number)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Report with RFI_Number "{rfi_number}" not found.'
        )
    report_dict = {
        k: v for k, v in report.__dict__.items()
        if not k.startswith("_")
    }
    return report_dict


@router.get("/suggest_report_no/", summary='پیشنهاد شماره گزارش', status_code=status.HTTP_200_OK)
def suggest_report_no(
    rfi_numbering: str,
    report_no: str,
    rev_no: RevType,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    result = find_report_no(rfi_numbering, report_no, rev_no, db)

    return result.get('suggested_report_no')

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_report(data: ReportCreateSchema, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    try:
        new_item = insert_new_report(db, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create report: {str(e)}"
        )
    return {"message": "Created new report successfully", "data": new_item}


@router.put("/{rfi_numbering}", status_code=status.HTTP_200_OK)
def update_report(
    rfi_numbering: str,
    data: ReportUpdateSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    report = get_report_by_rfi(db, rfi_numbering)
    if isinstance(data, list):
        for item in data:
            report = update_report_fields(report, item)
    else:
        report = update_report_fields(report, data)

    report = commit_report_update(db, report)
    return {"message": "Report updated successfully", "data": report}


@router.delete("/report/", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_no: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = get_report_by_report_number(db, report_no)
    delete_report_commit(db, report)
    return {"message": "Report deleted successfully"}
