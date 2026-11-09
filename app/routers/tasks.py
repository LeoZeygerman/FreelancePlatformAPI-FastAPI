from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.models.projects import ProjectsOrm
from app.models.tasks import TasksOrm
from app.models.users import UsersOrm
from app.schemas.tasks import CreateTask, ResponseTask


router = APIRouter(prefix='/task', tags=['Задачи проекта'])


@router.get('/create', summary='Добавить задачу', response_model=ResponseTask)
async def create_task_router(session: SessionDep, customer_id: int, task: CreateTask):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == customer_id)
    )

    if user.role != 'customer':
        raise HTTPException(status_code=404, detail='Только customer может добавлять задачи!')

    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == task.project_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail='Такого проекта нет!')
    elif project.customer_id != customer_id:
        raise HTTPException(status_code=404, detail='Только создатель проекта может добавлять задачи!')

    new_task = TasksOrm(
        task = task.task,
        description = task.description,
        deadline = task.deadline,
        status = task.status,
    )