from pydantic import BaseModel, ConfigDict

from schemas import UserReadSchema, TaskReadSchema


class ProjectCreateSchema(BaseModel):
    name: str
    description: str
    owner_id: int


class ProjectReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    owner: UserReadSchema
    tasks: list[TaskReadSchema] | None
