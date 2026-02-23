from sqlalchemy.orm import Session
from database.models.User import User
from core.hashing import Hasher


def get_user(username:str,db: Session):
    user = db.query(User).filter(User.user_name == username).first()
    return user

def get_user_by_username(db: Session, user_name: str):
    return db.query(User).filter(User.user_name == user_name).first()


def create_user(db: Session, user_data):
    new_user = User(
        user_name=user_data.user_name,
        password=Hasher.get_password_hash(user_data.password),
        permit=user_data.permit,
        unit=user_data.unit
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user: User, user_data):
    if user_data.password is not None:
        user.password = Hasher.get_password_hash(user_data.password)
    if user_data.permit is not None:
        user.permit = user_data.permit
    if user_data.unit is not None:
        user.unit = user_data.unit

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()