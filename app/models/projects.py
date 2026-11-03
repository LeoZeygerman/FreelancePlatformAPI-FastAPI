from sqlalchemy import ForeignKey
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Projects(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    budget: Mapped[int]
    customer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    developer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[int] = mapped_column(ForeignKey('payments.id'))