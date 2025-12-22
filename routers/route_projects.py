from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from database.repository.get_next_rfi_number import get_full_rfi_info
from database.session import get_db
from database.models import Project
from database.repository.project import get_all_projects
from database.repository.get_IRNNO import get_project_last_irnn
from database.repository.create_new_project import insert_new_project
from routers.route_login import get_current_user
from schemas.Project import ProjectCreate


router = APIRouter()

@router.get("/", summary="دریافت لیست نام پروژه‌ها")
def list_projects(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = get_all_projects(db)
    get_project_last_irnn(db, '', '')
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="هیچ پروژه‌ای یافت نشد"
        )

    # خروجی: دیکشنری id:name
    return {project.IDP: project.Title for project in projects}


@router.get('/{project_name}/irnno', summary='دریافت اخرین عدد irnno برای هر پروژه')
def retrieve_irnno(project_name: str, Over_Domestic: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_project_last_irnn(db, project_name, Over_Domestic)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'IRNNO for project "{project_name}" with type "{Over_Domestic}" not found.'
        )
    return data


@router.get("/{idp}/rfi/next", summary="بازگرداندن شماره rfi_number و idom")
def get_full_rfi_data(idp, in_out, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if in_out == '0':
            in_out_type = 'خارجی'
        elif in_out == '1':
            in_out_type = 'داخلی کالا'
        elif in_out == '2':
            in_out_type = 'داخلی کشتی'
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Invalid in_out value: "{in_out}"'
            )

        idom, next_rfi = get_full_rfi_info(db, idp, in_out_type)
        if idom is None or next_rfi is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'RFI information not found for project IDP "{idp}" and type "{in_out_type}"'
            )

        return {"IDOM": idom, "next_rfi_numbering": next_rfi}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving RFI data: {str(e)}"
        )


@router.post("/projects")
def create_new_project(data: ProjectCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.Title == data.Title).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Title "{data.Title}" already exists.'
        )
    try:
        new_item = insert_new_project(db, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )

    return {"message": "Created new project successfully", "data": new_item.IDP}
