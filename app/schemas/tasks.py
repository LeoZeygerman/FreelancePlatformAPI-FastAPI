from datetime import date

from pydantic import BaseModel, Field, field_validator


class CreateTask(BaseModel):
    customer_id: int
    project_id: int
    task: str = Field(max_length=50)
    description: str = Field(max_length=300)
    deadline: date
    status: bool

    @field_validator('deadline')
    @classmethod
    def validate_date(cls, value):
        if value < date.today():
            raise ValueError('Дедлайн не может быть в прошедшем времени!')
        return value