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
    developer_projects: list[ResponseShortProject] | None = None
    customer_projects: list[ResponseShortProject] | None = None
    rating: float | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class ResponseUserShort(BaseModel):
    id: int
    username: str
    role: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ResponseDeveloperStats(BaseModel):
    id: int
    username: str
    email: EmailStr
    rating: float | None = None
    projects_count: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ResponseCustomerWithProjects(BaseModel):
    id: int
    username: str
    email: EmailStr
    rating: float
    project_title: str
    project_budget: int
    project_status: bool

    model_config = ConfigDict(from_attributes=True)