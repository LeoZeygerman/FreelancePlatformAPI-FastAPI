from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func
from app.models.projects import ProjectsOrm


class PaymentsOrm(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    amount: Mapped[int]
    status: Mapped[bool]
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        func.now()
    )

    project: Mapped['ProjectsOrm'] = relationship(
        back_populates = 'payment_status'
    )