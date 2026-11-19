from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.applications import CreateApplication
from app.services.lookups import get_project_by_id


async def create_application(session: AsyncSession, application: CreateApplication):
    project = await get_project_by_id(session, application.project_id)

    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == application.developer_email)
    )

    new_application = ApplicationsOrm(
        project = project,
        developer = developer,
        cover_letter = application.cover_letter
    )

    session.add(new_application)
    await session.commit()
    return await get_application_by_id(session, new_application.id)


async def get_application_by_id(session: AsyncSession, application_id: int):
    application = await session.scalar(
        select(ApplicationsOrm)
        .where(ApplicationsOrm.id == application_id)
        .options(
            selectinload(ApplicationsOrm.developer),
            selectinload(ApplicationsOrm.project)
        )
    )
    return application


async def get_free_projects(session: AsyncSession):
    projects = await session.scalars(
        select(ProjectsOrm)
        .where(ProjectsOrm.developer_id == None)
    )
    result = projects.all()
    return result