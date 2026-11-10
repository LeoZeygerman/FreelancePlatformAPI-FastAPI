from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.applications import CreateApplication, ResponseApplication


router = APIRouter(prefix='/application', tags=['Заявки'])


@router.post('/create', summary='Добавить заявку', response_model=ResponseApplication)
async def create_application_router(session: SessionDep, application: CreateApplication):
    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == application.project_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    
    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == application.developer_email)
    )
    if developer is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    elif developer.role != 'developer':
        raise HTTPException(status_code=403, detail='Только разработчик может оставлять заявку!')

    new_application = ApplicationsOrm(
        project = project,
        developer = developer,
        cover_letter = application.cover_letter
    )

    session.add(new_application)
    await session.flush()
    await session.commit()
    return new_application


@router.get('/{application_id}', summary='Найти заявку', response_model=ResponseApplication)
async def get_application_by_id(session: SessionDep, application_id: int):
    application = await session.scalar(
        select(ApplicationsOrm)
        .where(ApplicationsOrm.id == application_id)
        .options(
            selectinload(ApplicationsOrm.developer),
            selectinload(ApplicationsOrm.project)
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail='Заявка не найдена!')
    return application