from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import User


def get_all_users(session: Session) -> list[User]:
    return list(session.scalars(select(User)).all())

def create_user(session: Session, user_data: UserCreateSchema) -> User:
    db_user = User(
        **user_data.model_dump()
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user