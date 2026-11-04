from datetime import datetime
from enum import StrEnum

from sqlalchemy import Table, Column, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class TaskStatusEnum(StrEnum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


task_assignees = Table(
    "tasks_assignees",
    Base.metadata,
    Column(
        "tasks_id",
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatusEnum] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    assignees: Mapped[list["User"]] = relationship(
        "User",
        secondary="task_assignees",
        back_populates="tasks"
    )
