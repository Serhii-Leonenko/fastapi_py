from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from db.models import Project, Task, User
from schemas import ProjectCreateSchema


class OwnerNotFoundError(Exception):
    pass


def _get_owner_by_id(db_session: AsyncSession, owner_id: int):
    return db_session.get(User, owner_id)


async def get_projects_list(
    db_session: AsyncSession,
    owner_id: int | None = None,
):
    statement = select(Project).options(
        joinedload(Project.owner),
        selectinload(Project.tasks).selectinload(Task.assignees),
    )

    if owner_id:
        if not await _get_owner_by_id(db_session, owner_id):
            raise OwnerNotFoundError("Owner with such id not found")

        statement = statement.where(Project.owner_id == owner_id)

    result = await db_session.scalars(statement)

    return list(result.all())


async def create_project(
    db_session: AsyncSession,
    project_data: ProjectCreateSchema,
) -> Project:
    project = Project(**project_data.model_dump())
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project, ["owner", "tasks"])

    return project
