from sqlalchemy.orm import Session
from database.models.T_Project import Project

def get_all_projects(db: Session):
    return db.query(Project).order_by(Project.Title.asc()).all()
