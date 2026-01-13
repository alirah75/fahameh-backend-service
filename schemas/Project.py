from pydantic import BaseModel


class ProjectCreateSchema(BaseModel):
    Title: str
    project_code: str