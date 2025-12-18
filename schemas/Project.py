from pydantic import BaseModel


class ProjectCreate(BaseModel):
    Title: str
    project_code: str