from pydantic import BaseModel, ConfigDict, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = 'cusotmer'
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
    project: ResponseShortProject | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
