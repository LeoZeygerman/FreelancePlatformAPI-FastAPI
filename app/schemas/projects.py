from pydantic import BaseModel, Field


class CreateProject(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    budget: int
    customer_id: int


class ResponseProject(BaseModel):
    pass