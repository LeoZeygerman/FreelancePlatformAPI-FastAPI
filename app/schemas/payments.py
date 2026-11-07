from pydantic import BaseModel


class CreatePayments(BaseModel):
    project_id: int
    amount: int