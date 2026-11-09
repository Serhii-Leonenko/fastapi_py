from datetime import datetime

from sqlalchemy import String, Text, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="projects")

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
