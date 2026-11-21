from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.applications import CreateApplication, ResponseApplication, ResponseApplicationByDeveloperRating, UpdateApplication
from app.schemas.projects import ResponseProjectShort
from app.services.applications import create_application, delete_application, get_application_by_id, get_applications_by_rating, get_free_projects, update_application


router = APIRouter(prefix='/application', tags=['Заявки'])


@router.get('/projects', summary='Свободные проекты для подачи заявки', response_model=list[ResponseProjectShort])
async def get_free_projects_router(session: SessionDep):
    projects = await get_free_projects(session)
    return projects


@router.post('/create', summary='Добавить заявку', response_model=ResponseApplication)
async def create_application_router(session: SessionDep, application: CreateApplication):
    new_application = await create_application(session, application)
    return new_application


@router.get('/get-one/{application_id}', summary='Найти заявку', response_model=ResponseApplication)
async def get_application_by_id_router(session: SessionDep, application_id: int):
    application = await get_application_by_id(session, application_id)
    return application


@router.get('/by-developers-rating', summary='Показать заявки по рейтингу разработчиков', response_model=list[ResponseApplicationByDeveloperRating])
async def get_applications_by_rating_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100)):
    applications = await get_applications_by_rating(session, limit)
    return applications


@router.patch('/update/{application_id}', summary='Отредактировать заявку', response_model=ResponseApplication)
async def update_application_router(session: SessionDep, application_id: int, developer_id: int, data: UpdateApplication):
    application = await update_application(session, application_id, developer_id, data)
    return application


@router.delete('/delete/{application_id}', summary='Удаление заявки')
async def delete_application_router(session: SessionDep, developer_id: int, application_id: int):
    application = await delete_application(session, developer_id, application_id)
    return application