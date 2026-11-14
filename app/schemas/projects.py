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
    budget: float = Field(gt=0)
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
    budget: float
    customer: ResponseUserForProject
    developer: ResponseUserForProject | None = None
    status: bool
    project_task: list[ResponseTaskForProject] | None = None

    model_config = ConfigDict(from_attributes=True)


class ResponseProjectShort(BaseModel):
    id: int
    title: str
    description: str
    budget: float
    status: bool


class ResponseProjectWithApplications(BaseModel):
    project_id: int
    project_title: str
    applications: int | None = None


class UpdateProject(BaseModel):
    title: str | None = None
    description: str | None = None
    budget: float | None = None
    status: bool | None = None
    developer_rating: int | None = Field(default=None, gt=0, le=5)
    customer_rating: int | None = Field(default=None, gt=0, le=5)