from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.projects import ProjectsOrm


class TasksOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[date]
    status: Mapped[bool] = mapped_column(default=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))

    project: Mapped['ProjectsOrm'] = relationship(
        back_populates='project_task'
    )
