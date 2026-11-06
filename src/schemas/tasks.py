from pydantic import BaseModel, Field

from db.models.tasks import TaskStatusEnum
from schemas import UserReadSchema


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    assignees: list[int] = Field(default_factory=list)
    project_id: int


class TaskReadSchema(BaseModel):
    id: int
    title: str
    status: TaskStatusEnum
    description: str
    assignees: list[UserReadSchema]


class TaskUpdateSchema(BaseModel):
    status: TaskStatusEnum | None = None
    assignees: list[int] | None = None
