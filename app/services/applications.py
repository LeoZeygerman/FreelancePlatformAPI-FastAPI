from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import ApplicationAlreadyExistsError, NotFoundError, AccessDeniedError
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.applications import CreateApplication, UpdateApplication
from app.services.lookups import get_project_by_id, get_user_by_id


async def get_application_by_id(session: AsyncSession, application_id: int) -> ApplicationsOrm:
    application = await session.scalar(
        select(ApplicationsOrm)
        .where(ApplicationsOrm.id == application_id)
        .options(
            selectinload(ApplicationsOrm.developer),
            selectinload(ApplicationsOrm.project)
        )
    )

    if application is None:
        raise NotFoundError('Заявка не найдена!')
    return application


async def get_free_projects(session: AsyncSession) -> list[ProjectsOrm]:
    """
    Retrieve available projects without assigned developers.

    Return projects that are not completed and
    do not have a developer assigned.
    """
    projects = await session.scalars(
        select(ProjectsOrm)
        .where(
            ProjectsOrm.developer_id == None,
            ProjectsOrm.status == False
        )
    )

    result = projects.all()
    if len(result) == 0:
        raise NotFoundError('Проекты не найдены!')
    return result


async def get_applications_by_rating(session: AsyncSession, limit: int) -> list[ApplicationsOrm]:
    """
    Retrieve applications ranked by developer rating.

    Sort applications by the developers' ratings
    in descending order, with the highest-rated first.
    """
    query = await session.execute(
        select(
            ApplicationsOrm.project_id,
            ProjectsOrm.title.label('project_title'),
            ProjectsOrm.budget.label('project_budget'),
            ApplicationsOrm.developer_id,
            UsersOrm.username.label('developer_name'),
            UsersOrm.role,
            UsersOrm.rating.label('developer_rating')
        )
        .where(
            ApplicationsOrm.developer_id.is_not(None),
            UsersOrm.role == 'developer'
        )
        .join(ProjectsOrm, ProjectsOrm.id == ApplicationsOrm.project_id)
        .join(UsersOrm, UsersOrm.id == ApplicationsOrm.developer_id)
        .order_by(UsersOrm.rating.desc())
        .limit(limit)
    )

    applications = query.mappings().all()
    if len(applications) == 0:
        raise NotFoundError('Заявки не найдены!')
    return applications


async def create_application(session: AsyncSession, application: CreateApplication) -> ApplicationsOrm:
    project = await get_project_by_id(session, application.project_id)
    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == application.developer_email)
    )
    if developer is None:
        raise NotFoundError('Разработчик не найден!')
    elif developer.role != 'developer':
        raise NotFoundError('Пользователь не разработчик!')

    new_application = ApplicationsOrm(
        project = project,
        developer = developer,
        cover_letter = application.cover_letter
    )

    session.add(new_application)
    await session.flush()

    check = await session.scalar(
        select(func.count(ApplicationsOrm))
        .where(
            ApplicationsOrm.project_id == application.project_id,
            ApplicationsOrm.developer_id == developer.id
        )
    )
    if check > 1:
        raise ApplicationAlreadyExistsError()

    await session.commit()
    return await get_application_by_id(session, new_application.id)


async def update_application(session: AsyncSession, application_id: int, developer_id: int, data: UpdateApplication) -> ApplicationsOrm:
    application = await get_application_by_id(session, application_id)
    if application.developer_id != developer_id:
        raise AccessDeniedError()
    await get_user_by_id(session, developer_id)

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(application, key, value)

    await session.commit()
    return await get_application_by_id(session, application_id)


async def delete_application(session: AsyncSession, developer_id: int, application_id: int) -> dict:
    developer = await get_user_by_id(session, developer_id)
    application = await get_application_by_id(session, application_id)
    if application.developer_id != developer_id:
        raise AccessDeniedError()

    await session.delete(application)
    await session.commit()
    return {'msg': f'Заявка {application_id} удалена!'}
