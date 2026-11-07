from pydantic import BaseModel, ConfigDict, Field


class CreateApplication(BaseModel):
    project_id: int
    develioer_id: int
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


class UpdateApplication(BaseModel):
    cover_letter: str | None = Field(default=None, max_length=250)
