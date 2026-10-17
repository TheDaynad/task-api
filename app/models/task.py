from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.base import Base
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User

class Task(Base):
    __tablename__ = 'tasks'
    id :Mapped[int] = mapped_column(primary_key=True)
    title :Mapped[str] = mapped_column()
    description :Mapped[str | None] = mapped_column(nullable=True)
    is_completed :Mapped[bool] = mapped_column()
    user_id :Mapped[int] = mapped_column(ForeignKey('users.id'))
    user :Mapped["User"] = relationship('User', back_populates='tasks')