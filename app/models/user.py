from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.task import Task


class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column()
    email : Mapped[str] = mapped_column()
    is_active : Mapped[bool] = mapped_column()
    tasks: Mapped[list["Task"]] = relationship('Task', back_populates='user')
