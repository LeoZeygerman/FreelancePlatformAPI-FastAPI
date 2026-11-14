from datetime import date
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class TaskPriority(str, Enum):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'


class CreateTask(BaseModel):
    project_id: int
    task: str = Field(max_length=50)
    description: str = Field(max_length=300)
    priority: TaskPriority
    deadline: date

    @field_validator('deadline')
    @classmethod
    def validate_date(cls, value):
        if value is not None and value < date.today():
            raise ValueError('Дедлайн не может быть в прошедшем времени!')
        return value


class ResponseProjectForTask(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ResponseTask(BaseModel):
    task: str
    description: str
    priority: str
    deadline: date
    status: bool
    project: ResponseProjectForTask

    model_config = ConfigDict(from_attributes=True)


class UpdateTask(BaseModel):
    task: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=300)
    priority: TaskPriority | None = None
    deadline: date | None = None
    status: bool | None = None

    @field_validator('deadline')
    @classmethod
    def validate_date(cls, value):
        if value is not None and value < date.today():
            raise ValueError('Дедлайн не может быть в прошедшем времени!')
        return value