from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.tasks import create_task, update_task, delete_task, AssigneeNotFoundError, TaskNotFoundError
from src.db import get_db_session
from src.schemas.tasks import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema


router = APIRouter(tags=["tasks"])


@router.post("/tasks", response_model=TaskReadSchema)
async def create_task_endpoint(
    task_data: TaskCreateSchema,
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    try:
        return await create_task(
            db_session=db_session,
            task_data=task_data
    )
    except AssigneeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/tasks/{task_id}", response_model=TaskReadSchema)
async def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdateSchema,
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    try:
        return await update_task(db_session=db_session, task_id=task_id, task_data=task_data)
    except (TaskNotFoundError, AssigneeNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/tasks/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        await delete_task(db_session=db, task_id=task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
