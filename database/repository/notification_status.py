from sqlalchemy.orm import Session
from database.models.notification_status import NotificationStatus

def get_all_notification_statuses(db: Session):
    return db.query(NotificationStatus).order_by(NotificationStatus.id.asc()).all()