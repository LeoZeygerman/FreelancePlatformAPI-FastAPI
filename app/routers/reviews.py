from pydantic import BaseModel


class CreateReview(BaseModel):
    project_id: int
    reviewer_id: int
    reviewee_id: int
    rating: float