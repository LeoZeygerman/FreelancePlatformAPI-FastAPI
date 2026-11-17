from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UsersOrm
from app.schemas.users import CreateUser


async def create_user(session: AsyncSession, user: CreateUser):
    new_user = UsersOrm(
        username = user.username,
        role = user.role,
        email = user.email
    )
    session.add(new_user)
    await session.commit()
    return await get_user_by_email(session, user.email)


async def get_user_by_email(session: AsyncSession, user_email: EmailStr):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == user_email)
    )
    return user