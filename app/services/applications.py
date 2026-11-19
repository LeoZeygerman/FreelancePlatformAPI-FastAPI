from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.applications import ApplicationsOrm
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
    return 


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