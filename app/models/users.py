from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.projects import ProjectsOrm

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True) 
    username: Mapped[str]
    role: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    developer_projects: Mapped[list['ProjectsOrm']] = relationship(
        back_populates = 'developer'
    )

    customer_projects: Mapped[list['ProjectsOrm']] = relationship(
        back_populates = 'customer'
    )
