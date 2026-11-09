from datetime import date
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreateTask(BaseModel):
    project_id: int
    task: str = Field(max_length=50)
    description: str = Field(max_length=300)
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
    deadline: date
    status: bool
    project: ResponseProjectForTask

    model_config = ConfigDict(from_attributes=True)


class UpdateTask(BaseModel):
    task: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=300)
    deadline: date | None = None
    status: bool | None = None

    @field_validator('deadline')
    @classmethod
    def validate_date(cls, value):
        if value is not None and value < date.today():
            raise ValueError('Дедлайн не может быть в прошедшем времени!')
        return value