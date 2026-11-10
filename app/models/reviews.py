from sqlalchemy import ForeignKey
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.projects import ProjectsOrm
    from app.models.users import UsersOrm


class ReviewsOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    reviewer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    reviewee_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[float] = mapped_column(default=None)

    reviewee_project: Mapped['ProjectsOrm'] = relationship(
        foreign_keys = project_id,
        back_populates = 'project_reviews'
    )

    reviewer: Mapped['UsersOrm'] = relationship(
        foreign_keys=reviewer_id,
        back_populates='user_reviews'
    )

    reviewee: Mapped['UsersOrm'] = relationship(
        foreign_keys=reviewee_id,
        back_populates='user_rating'
    )