from pydantic import BaseModel, Field


class CreateReview(BaseModel):
    project_id: int
    reviewer_id: int
    reviewee_id: int
    rating: float = Field(ge=1, le=5)


class UpdateReview(BaseModel):
    rating: float | None = Field(default=None, ge=1, le=5)