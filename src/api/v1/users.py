from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from crud.users import get_all_users, create_user, get_user_by_email
from db import get_db_session


router = APIRouter(tags=["users"])


@router.get("/users/", response_model=list[schemas.UserReadSchema])
async def list_users(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    return await get_all_users(session=db_session)


@router.post("/users/", response_model=schemas.UserReadSchema)
async def user_create(user_data: schemas.UserCreateSchema, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    if await get_user_by_email(session=db_session, email=user_data.email):
        raise HTTPException(
            status_code=409,
            detail="User with this email already exist"
        )

    return await create_user(session=db_session, user_data=user_data)
