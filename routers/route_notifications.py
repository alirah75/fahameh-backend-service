from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.repository.create_new_inspection import insert_new_rfi_date
from database.repository.create_new_rfi_date import insert_in_rfi_date
from database.repository.delete_one_notification import delete_notification_service, delete_one_date_service
from database.repository.update_one_notification import update_notif, update_time_table_info
from database.session import get_db
from database.repository.get_one_notif import find_notif
from database.repository.create_time_table import insert_in_timetable
from routers.route_login import get_current_user
from schemas.TimeTable import TimeTableCreateSchema, RFIDateUpdateSchema, NotificationUpdateSchema, \
    AddInspectionDateSchema

router = APIRouter()


@router.get("/statuses", summary="دریافت لیست وضعیت‌های ممکن برای نوتیفیکیشن‌ها", status_code=status.HTTP_200_OK)
def list_notification_statuses(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return {1: 'Cancel', 2: 'Done', 3: 'Ongoing'}


@router.get('/{rfi_number}', summary='نمایش اطلاعات یک نوتیف', status_code=status.HTTP_200_OK)
def retrieve_one_notification(rfi_number, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    one_note = find_notif(db, rfi_number)
    if not one_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Notification with RFI_Number "{rfi_number}" not found.'
        )
    return one_note


# @router.get('/{report_number}', summary='نمایش اطلاعات یک نوتیف')
# def retrieve_one_notification(report_number, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     one_note = find_notif(db, report_number)
#     if not one_note:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'Notification with RFI_Number "{report_number}" not found.'
#         )
#     return one_note

@router.post(
    "/add-inspection-dates",
    summary="ایجاد تاریخ بازرسی جدید",
    status_code=status.HTTP_201_CREATED
)
def create_inspection_date(
    data: AddInspectionDateSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_row = insert_new_rfi_date(db, data)

    return new_row



@router.post("/", summary="ساخت نوتیفیکشن جدید", status_code=status.HTTP_201_CREATED)
def create_timetable_api(data: TimeTableCreateSchema, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    from database.models import TimeTable
    existing = db.query(TimeTable).filter(
        TimeTable.IDP == data.IDP,
                TimeTable.IDOM == data.IDOM,
                TimeTable.Over_Domestic == data.Over_Domestic,
                TimeTable.RFI_Number == data.RFI_Number
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This TimeTable record already exists."
        )

    try:
        new_item, rfi_numbering = insert_in_timetable(db, data)
        new_rfi_date = insert_in_rfi_date(db, data, rfi_numbering)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create notification: {str(e)}"
        )
    return {"message": "Created new notification successfully", "data": new_item}


@router.put('/{rfi_number}', summary='آپدیت اطلاعات روز های بازرسی', status_code=status.HTTP_200_OK)
def update_rfi_date(
    rfi_number: str,
    payload: RFIDateUpdateSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_notif(db, rfi_number, payload, current_user)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Notification with RFI_Number "{rfi_number}" not found.'
        )

    return {
        "message": "Notification updated successfully",
        "data": updated
    }


@router.put('/notification/', summary='آپدیت اطلاعات نوتیفیکیشن', status_code=status.HTTP_200_OK)
def update_time_table(
    rfi_number: str,
    payload: NotificationUpdateSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_time_table_info(db, rfi_number, payload, current_user)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Notification with RFI_Number "{rfi_number}" not found.'
        )

    return {
        "message": "Notification updated successfully",
        "data": updated
    }


@router.delete("/notification/", summary="Delete notification and related data", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    rfi_numbering,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_notification_service(db, rfi_numbering)
    return {
        "message": "Notification and related data deleted successfully"
    }

@router.delete("/one_date/", summary="Delete one date", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_date(
    rfi_numbering,
    date_,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_one_date_service(db, rfi_numbering, date_)
    return {
        "message": "Notification and related data deleted successfully"
    }
