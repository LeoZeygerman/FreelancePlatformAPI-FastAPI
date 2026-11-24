from fastapi import APIRouter, Query
from app.database import SessionDep
from app.schemas.projects import CreateProject, ResponseProject, ResponseProjectShort, UpdateProject, ResponseProjectWithApplicationCount
from app.schemas.reviews import CreateReview
from app.services.projects import add_mark, create_project, delete_project, get_all_projects, get_best_paid_projects, get_project_with_relations, get_projects_by_applications, update_project, add_developer_in_project


router = APIRouter(prefix='/project', tags=['Проекты'])


@router.get('/get-one/{project_id}', summary='Найти проект по ID', response_model=ResponseProject)
async def get_project_by_id_router(session: SessionDep, project_id: int):
    project = await get_project_with_relations(session, project_id)
    return project


@router.post('/create', summary='Создать проект', response_model=ResponseProject)
async def create_project_router(session: SessionDep, project: CreateProject):
    new_project = await create_project(session, project)
    return new_project


@router.patch('/add-developer', summary='Добавить разработчика в проект')
async def add_developer_in_project_router(session: SessionDep, customer_id: int, developer_id: int, project_id: int):
    result = await add_developer_in_project(session, customer_id, developer_id, project_id)
    return result


@router.get('/all', summary='Получить все проекты', response_model=list[ResponseProjectShort])
async def get_all_projects_router(session: SessionDep):
    projects = await get_all_projects(session)
    return projects


@router.get('/by-paid', summary='Получить самые высокооплачиваемые проекты', response_model=list[ResponseProjectShort])
async def get_best_paid_projects_router(session: SessionDep, limit: int = Query(ge=1, default=10, le=100)):
    projects = await get_best_paid_projects(session, limit)
    return projects


@router.get('/by-applications', summary='Получить проекты по количеству заявок', response_model=list[ResponseProjectWithApplicationCount])
async def get_projects_by_applications_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100)):
    projects = await get_projects_by_applications(session, limit)
    return projects


@router.patch('/update/{project_id}', summary='Обновить проект', response_model=ResponseProject)
async def update_project_router(session: SessionDep, project_id: int, data: UpdateProject, user_id: int):
    project = await update_project(session, project_id, data, user_id)
    return project


@router.post('/add-mark/{project_id}', summary='Выставить оценку')
async def add_mark_router(session: SessionDep, project: CreateReview, project_id: int):
    new_mark = await add_mark(session, project, project_id)
    return new_mark


@router.delete('/delete/{project_id}', summary='Удалить проект')
async def delete_project_router(session: SessionDep, project_id: int, user_id: int):
    project = await delete_project(session, project_id, user_id)
    return project