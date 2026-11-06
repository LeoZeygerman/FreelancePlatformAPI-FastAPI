from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class CreateProject(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    budget: int
    customer_id: int


class ResponseUserForProject(BaseModel):
    username: str
    email: str


class ResponseTaskForProject(BaseModel):
    task: str
    description: str
    deadline: date
    status: bool


class ResponseProject(BaseModel):
    title: str
    description: str
    budget: str
    customer: ResponseUserForProject
    developer: list[ResponseUserForProject] | None = None
    status: bool
    project_task: list[ResponseTaskForProject] | None = None

    model_config = ConfigDict(from_attributes=True)