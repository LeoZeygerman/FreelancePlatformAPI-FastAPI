from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.tasks import CreateTask, ResponseTask, TaskPriority, UpdateTask
from app.services.tasks import create_task, delete_task, get_task_by_id, get_tasks_by_priority, update_tasks


router = APIRouter(prefix='/task', tags=['Задачи проекта'])


@router.post('/create', summary='Добавить задачу', response_model=ResponseTask)
async def create_task_router(session: SessionDep, customer_id: int, task: CreateTask):
    new_task = await create_task(session, customer_id, task)
    return new_task


@router.get('/{task_id}', summary='Найти задачу по ID', response_model=ResponseTask)
async def get_task_by_id_router(session: SessionDep, task_id: int, customer_id: int):
    task = await get_task_by_id(session, task_id, customer_id)
    return task


@router.get('/{project_id}/by-priority', summary='Получить задачи по приоритету', response_model=list[ResponseTask])
async def get_tasks_by_priority_router(session: SessionDep, project_id: int, priority: TaskPriority):
    tasks = await get_tasks_by_priority(session, project_id, priority)
    return tasks


@router.patch('/update/{task_id}', summary='Обновить задачу', response_model=ResponseTask)
async def update_task_router(session: SessionDep, task_id: int, data: UpdateTask, customer_id: int):
    task = await update_tasks(session, task_id, data, customer_id)
    return task


@router.delete('/delete/{task_id}', summary='Удаление задачи')
async def delete_task_router(session: SessionDep, task_id: int, customer_id: int):
    task = await delete_task(session, task_id, customer_id)
    return task
