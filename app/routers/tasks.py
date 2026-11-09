from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.projects import ProjectsOrm
from app.models.tasks import TasksOrm
from app.models.users import UsersOrm
from app.schemas.tasks import CreateTask, ResponseTask, UpdateTask


router = APIRouter(prefix='/task', tags=['Задачи проекта'])


@router.post('/create', summary='Добавить задачу', response_model=ResponseTask)
async def create_task_router(session: SessionDep, customer_id: int, task: CreateTask):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == customer_id)
    )

    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    elif user.role != 'customer':
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
        project = project,
        task = task.task,
        description = task.description,
        deadline = task.deadline,
    )
    session.add(new_task)
    await session.commit()
    return new_task


@router.get('/{task_id}', summary='Найти задачу по ID', response_model=ResponseTask)
async def get_task_by_id(session: SessionDep, task_id: int):
    task = await session.scalar(
        select(TasksOrm)
        .where(TasksOrm.id == task_id)
        .options(
            selectinload(TasksOrm.project)
        )
    )
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена!')
    return task


@router.patch('/update/{task_id}', summary='Обновить задачу', response_model=ResponseTask)
async def update_task_router(session: SessionDep, task_id: int, data: UpdateTask):
    task = await session.scalar(
        select(TasksOrm)
        .where(TasksOrm.id == task_id)
        .options(
            selectinload(TasksOrm.project)
        )
    )
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена!')

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(task, key, value)

    await session.flush()
    await session.commit()
    return task


@router.delete('/delete/{task_id}', summary='Удаление задачи')
async def delete_task_router(session: SessionDep, task_id: int):
    task = await session.scalar(
        select(TasksOrm)
        .where(TasksOrm.id == task_id)
    )
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена!')

    await session.delete(task)
    await session.commit()
    return {'msg': 'Задача удалена!'}
