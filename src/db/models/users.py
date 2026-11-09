from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    projects: Mapped["Project"] = relationship("Project", back_populates="owner")
    tasks: Mapped[list["Task"]] = relationship(
        "Task", secondary="tasks_assignees", back_populates="assignees"
    )
    password: Mapped[str] = mapped_column(String(255))

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
