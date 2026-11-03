from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from schemas.users import UserCreateSchema


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.scalars(select(User))

    return list(result.all())


async def create_user(session: AsyncSession, user_data: UserCreateSchema) -> User:
    db_user = User(
        **user_data.model_dump()
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    return await session.scalar(select(User).where(User.email == email))
