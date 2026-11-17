from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UsersOrm
from sqlalchemy.orm import selectinload


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