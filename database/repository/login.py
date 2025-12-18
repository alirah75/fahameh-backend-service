from sqlalchemy.orm import Session
from database.models.User import User


def get_user(username:str,db: Session):
    user = db.query(User).filter(User.user_name == username).first()
    return user