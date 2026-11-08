from app.models.applications import ApplicationsOrm
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.projects import ProjectsOrm


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True) 
    username: Mapped[str]
    role: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    rating: Mapped[float] = mapped_column(default=None)

    developer_projects: Mapped[list['ProjectsOrm']] = relationship(
        foreign_keys = 'ProjectsOrm.developer_id',
        back_populates = 'developer'
    )

    customer_projects: Mapped[list['ProjectsOrm']] = relationship(
        foreign_keys = 'ProjectsOrm.customer_id',
        back_populates = 'customer'
    )

    developer_applications: Mapped[list['ApplicationsOrm']] = relationship(
        back_populates = 'developer'
    )
