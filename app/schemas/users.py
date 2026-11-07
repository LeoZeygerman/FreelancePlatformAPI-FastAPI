from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = 'customer'
    DEVELOPER = 'developer'


class ResponseShortProject(BaseModel):
    id: int
    title: str
    budget: int

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    username: str
    role: UserRole
    email: EmailStr


class ResponseUser(BaseModel):
    username: str
    role: str
    email: str
    developer_project: list[ResponseShortProject] | None = None
    customer_project: list[ResponseShortProject] | None = None
    rating: int

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
