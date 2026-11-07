from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = 'customer'
    DEVELOPER = 'developer'


class ResponseShortProject(BaseModel):
    id: int
    title: str
    budget: int


class CreateUser(BaseModel):
    username: str
    role: UserRole
    email: EmailStr


class ResponseUser(BaseModel):
    username: str
    role: str
    email: str
    project: list[ResponseShortProject] | None = None
    rating: int

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
