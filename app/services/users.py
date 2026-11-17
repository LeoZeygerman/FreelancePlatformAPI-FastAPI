from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UsersOrm
from app.schemas.users import CreateUser
from sqlalchemy.orm import selectinload
from app.services.lookups import get_user_by_id

#TODO сделать оброботчик ошибок

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


async def get_all_users(session: AsyncSession):
    users = await session.scalars(
        select(UsersOrm)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    result = users.all()
    return result


async def get_user_by_id(session: AsyncSession, user_id: int):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    return user


async def get_developers_by_rating(session: AsyncSession, limit: int):
    developers = await session.execute(
        select(UsersOrm)
        .where(UsersOrm.role == 'developer')
        .options(
            selectinload(UsersOrm.customer_projects),
            selectinload(UsersOrm.developer_projects)
        )
        .order_by(UsersOrm.rating.desc().nullslast())
        .limit(limit)
    )

    result = developers.mappings().all()
    return result


