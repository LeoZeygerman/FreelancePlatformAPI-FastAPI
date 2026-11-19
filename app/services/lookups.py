from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm


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


async def get_project_by_id(session: AsyncSession, project_id: int):
    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == project_id)
    )
    return project