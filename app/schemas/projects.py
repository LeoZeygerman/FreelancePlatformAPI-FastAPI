from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateTaskForProject(BaseModel):
    task: str
    description: str = Field(max_length=250)
    deadline: date

    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, value):
        if value < date.today():
            raise ValueError('Дедлайн не может быть прошедшим!')
        return value


class CreateProject(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    budget: int
    customer_id: int
    project_task: list[CreateTaskForProject]


class ResponseUserForProject(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ResponseTaskForProject(BaseModel):
    task: str
    description: str
    deadline: date
    status: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseProject(BaseModel):
    id: int
    title: str
    description: str
    budget: int
    customer: ResponseUserForProject
    developer: ResponseUserForProject | None = None
    status: bool
    project_task: list[ResponseTaskForProject] | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateProject(BaseModel):
    title: str | None = None
    description: str | None = None
    budget: int | None = None
    status: bool | None = None