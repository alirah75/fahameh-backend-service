from pydantic import BaseModel
from typing import Optional, List


class ProjectBase(BaseModel):
    Title: Optional[str] = None
    Abbreviation: Optional[str] = None
    SubProject: Optional[str] = None
    Material_Code: Optional[str] = None
    Remark: Optional[str] = None


class ProjectCreate(ProjectBase):
    Title: str
    project_code: str


class ProjectUpdate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    IDP: int

    class Config:
        from_attributes = True