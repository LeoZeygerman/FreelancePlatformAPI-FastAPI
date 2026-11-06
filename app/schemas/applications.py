from pydantic import BaseModel, ConfigDict, Field


class CreateApplication(BaseModel):
    project_id: int
    develioer_id: int
    cover_letter: str = Field(max_length=250)

    model_config = ConfigDict(from_attributes=True)