from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.projects import ProjectsOrm
from app.models.tasks import TasksOrm
from app.schemas.projects import CreateProject, ResponseProject, CreateTaskForProject


router = APIRouter(prefix='/project', tags=['Проекты'])


@router.post('/create', summary='Создать проект', response_model=ResponseProject)
async def create_project_router(session: SessionDep, project: CreateProject, new_task: CreateTaskForProject):
    new_project = ProjectsOrm(
        title = project.title,
        description = project.description,
        budget = project.budget,
        customer_id = project.customer_id,
        project_task = TasksOrm(
            task = new_task.task,
            description = new_task.description,
            deadline = new_task.deadline
        )
    )
    session.add(new_project)
    await session.commit()
    await session.flush()
    return new_project


@router.get('/{project_id}', summary='Найти проект по ID', response_model=ResponseProject)
async def get_project_by_id_router(session: SessionDep, project_id: int):
    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == project_id)
        .options(
            selectinload(ProjectsOrm.customer),
            selectinload(ProjectsOrm.developer),
            selectinload(ProjectsOrm.payment_status),
            selectinload(ProjectsOrm.project_task),
            selectinload(ProjectsOrm.developer_applications)
        )
    )
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return project


