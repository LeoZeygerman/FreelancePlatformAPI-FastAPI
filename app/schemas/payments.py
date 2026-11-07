from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreatePayments(BaseModel):
    project_id: int
    amount: int


class ResponseProjectForPayments(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class ResponsePayments(BaseModel):
    id: int
    project: ResponseProjectForPayments
    amount: int
    status: bool
    created_at: datetime


class UpdatePayments(BaseModel):
    amount: int | None = None
    status: bool | None = None
