from sqlalchemy import ForeignKey
from app.models.tasks import TasksOrm
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.payments import PaymentsOrm
from app.models.users import UsersOrm


class ProjectsOrm(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    budget: Mapped[int]
    customer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    developer_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    status: Mapped[int] = mapped_column(ForeignKey('payments.id'))

    customer: Mapped['UsersOrm'] = relationship(
        foreign_keys = [customer_id],
        back_populates = 'customer_projects'
    )

    developer: Mapped['UsersOrm'] = relationship(
        foreign_keys = [developer_id],
        back_populates = 'developer_projects'
    )

    status: Mapped['PaymentsOrm'] = relationship(
        back_populates = 'project'
    )

    project_task: Mapped['TasksOrm'] = relationship(
        back_populates = 'project'
    )