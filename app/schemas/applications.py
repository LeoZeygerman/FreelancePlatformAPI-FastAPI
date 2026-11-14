from pydantic import BaseModel, ConfigDict, Field, EmailStr


class CreateApplication(BaseModel):
    project_id: int
    developer_email: EmailStr
    cover_letter: str = Field(max_length=250)


class ResponseProjectForApplication(BaseModel):
    title: str
    description: str
    budget: int

    model_config = ConfigDict(from_attributes=True)


class ResponseDeveloperForApplication(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ResponseApplication(BaseModel):
    project: ResponseProjectForApplication
    developer: ResponseDeveloperForApplication
    cover_letter: str

    model_config = ConfigDict(from_attributes=True)


class ResponseApplicationByDeveloperRating(BaseModel):
    project_id: int
    project_title: str
    project_budget: float
    developer_id: int
    developer_name: str
    developer_rating: float        


class UpdateApplication(BaseModel):
    cover_letter: str | None = Field(default=None, max_length=250)
