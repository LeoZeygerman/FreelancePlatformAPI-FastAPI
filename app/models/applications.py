from sqlalchemy import ForeignKey
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm


class ApplicationsOrm(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    developer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    cover_letter: Mapped[str] 

    project: Mapped['ProjectsOrm'] = relationship(
        foreign_keys=project_id,
        back_populates = 'developer_applications'
    )

    developer: Mapped['UsersOrm'] = relationship(
        foreign_keys=developer_id,
        back_populates='developer_applications'
    )