from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models import Task, User
from db.models.tasks import TaskStatusEnum
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema


class AssigneeNotFoundError(Exception):
    pass


class TaskNotFoundError(Exception):
    pass


class TaskAlreadyExistsError(Exception):
    pass


async def _get_assignees_by_ids(
    db_session: AsyncSession, assignee_ids: list[int]
) -> list[User]:
    result = await db_session.scalars(select(User).where(User.id.in_(assignee_ids)))
    found_assignees = {assignee.id: assignee for assignee in result.all()}

    missing_assignee_ids = set(assignee_ids) - set(found_assignees.keys())
    if missing_assignee_ids:
        raise AssigneeNotFoundError(
            f"Assignees with IDs: {missing_assignee_ids} not found"
        )

    return list(found_assignees.values())


async def get_task_by_id(db_session: AsyncSession, task_id: int) -> Task | None:
    stmt = select(Task).options(selectinload(Task.assignees)).where(Task.id == task_id)

    return await db_session.scalar(stmt)


async def create_task(
    db_session: AsyncSession, task_data: TaskCreateSchema
) -> Task:
    if await db_session.scalar(
            select(Task).where(Task.title == task_data.title, Task.project_id == task_data.project_id)):
        raise TaskAlreadyExistsError("Task with such title for this project already exists")

    task_data = task_data.model_dump()

    assignees = []
    if "assignees" in task_data:
        assignee_ids = task_data.pop("assignees")
        assignees = await _get_assignees_by_ids(db_session, assignee_ids)

    task = Task(
        **task_data,
        status=TaskStatusEnum.NEW,
        assignees=assignees,
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task, ["assignees"])

    return task


async def update_task(
    db_session: AsyncSession, task_id: int, task_data: TaskUpdateSchema
) -> Task:
    task = await get_task_by_id(db_session, task_id)
    if not task:
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    update_data = task_data.model_dump(exclude_unset=True)

    if "assignees" in update_data:
        assignee_ids = update_data.pop("assignees")
        task.assignees = await _get_assignees_by_ids(db_session, assignee_ids)

    for field, value in update_data.items():
        setattr(task, field, value)

    await db_session.commit()
    await db_session.refresh(task, ["assignees"])

    return task


async def delete_task(db_session: AsyncSession, task_id: int) -> None:
    task = await get_task_by_id(db_session, task_id)
    if not task:
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    await db_session.delete(task)
    await db_session.commit()
