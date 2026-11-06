from pydantic import BaseModel, ConfigDict, Field


class CreateApplication(BaseModel):
    project_id: int
    develioer_id: int
    cover_letter: str = Field(max_length=250)


class ResponseProjectForApplication(BaseModel):
    title: str
    description: str
    budget: int


class ResponseDeveloperForApplication(BaseModel):
        username: str
        email: str


class ResponseApplication(BaseModel):
    project: ResponseProjectForApplication
    developer: ResponseDeveloperForApplication
    cover_letter: str    


class UpdateApplication(BaseModel):
    cover_letter: str | None = Field(default=None, max_length=250)
