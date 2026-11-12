from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.applications import CreateApplication, ResponseApplication, UpdateApplication
from app.schemas.projects import ResponseProjectShort


router = APIRouter(prefix='/application', tags=['Заявки'])


@router.get('/projects', summary='Свободные проекты для подачи заявки', response_model=list[ResponseProjectShort])
async def get_free_projects_router(session: SessionDep):
    projects = await session.scalars(
        select(ProjectsOrm)
        .where(ProjectsOrm.developer_id == None)
    )
    result = projects.all()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail='Проекты не найдены!')
    return result


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


@router.patch('/update/{application_id}', summary='Отредактировать заявку', response_model=ResponseApplication)
async def update_application_router(session: SessionDep, application_id: int, developer_id: int, data: UpdateApplication):
    application = await session.scalar(
        select(ApplicationsOrm)
        .where(ApplicationsOrm.id == application_id)
        .options(
            selectinload(ApplicationsOrm.project),
            selectinload(ApplicationsOrm.developer)
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail='Заявка не найдена!')

    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == developer_id)
    )
    if developer is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    elif developer.id != application.developer_id:
        raise HTTPException(status_code=403, detail='Только разработчик, оставивший заявку, может ее редактировать!')

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(application, key, value)

    await session.commit()
    return application


@router.delete('/delete/{application_id}', summary='Удаление заявки')
async def delete_application_router(session: SessionDep, developer_id: int, application_id: int):
    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == developer_id)
    )
    if developer.role != 'developer':
        raise HTTPException(status_code=403, detail='Только developer может удалять заявку!')

    application = await session.scalar(
        select(ApplicationsOrm)
        .where(ApplicationsOrm.id == application_id)
    )
    if application is None:
        raise HTTPException(status_code=404, detail='Заявка не найдена!')
    elif application.developer_id != developer_id:
        raise HTTPException(status_code=403, detail='Только владелец заявки может ее удалить!')

    await session.delete(application)
    await session.commit()
    return {'msg': f'Заявка {application_id} успешно удалена!'}