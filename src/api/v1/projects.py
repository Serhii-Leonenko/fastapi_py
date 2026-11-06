from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from crud.projects import get_projects_list, create_project, OwnerNotFoundError
from db import get_db_session
from schemas import ProjectReadSchema, ProjectCreateSchema

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=list[ProjectReadSchema])
async def projects_list(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    owner_id: int | None = None,
):
    try:
        return await get_projects_list(db_session=db_session, owner_id=owner_id)
    except OwnerNotFoundError:
        raise HTTPException(status_code=404, detail="Owner not found")


@router.post("/projects", response_model=ProjectReadSchema)
async def project_create(
    project_data: ProjectCreateSchema,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await create_project(db_session=db_session, project_data=project_data)
