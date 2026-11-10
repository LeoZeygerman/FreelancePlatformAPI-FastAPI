from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CreatePayments(BaseModel):
    project_id: int
    amount: int = Field(gt=0)


class ResponseProjectForPayments(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class ResponsePayments(BaseModel):
    id: int
    project: ResponseProjectForPayments
    amount: int
    status: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdatePayments(BaseModel):
    amount: int | None = None
    status: bool | None = None
