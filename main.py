from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud.users import get_all_users, create_user, get_user_by_email
from db import get_db_session

app = FastAPI()


@app.get("/users/", response_model=list[schemas.UserReadSchema])
def list_users(db_session: Annotated[Session, Depends(get_db_session)]):
    return get_all_users(session=db_session)

@app.post("/user/create/", response_model=schemas.UserReadSchema)
def user_create(user_data: schemas.UserCreateSchema, db_session: Annotated[Session, Depends(get_db_session)]):
    if get_user_by_email(session=db_session, email=user_data.email):
        raise HTTPException(
            status_code=409,
            detail="User with this email already exist"
        )

    return create_user(session=db_session, user_data=user_data)
