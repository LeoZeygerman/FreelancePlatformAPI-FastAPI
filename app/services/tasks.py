from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.exceptions import NotFoundError, AccessDeniedError
from app.models.tasks import TasksOrm
from app.schemas.tasks import CreateTask, UpdateTask
from app.services.lookups import get_project_by_id, get_user_by_id


async def create_task(session: AsyncSession, customer_id: int, task: CreateTask) -> TasksOrm:
    project = await get_project_by_id(session, task.project_id)
    user = await get_user_by_id(session, customer_id)
    if project.customer_id != user.id:
        raise AccessDeniedError()

    new_task = TasksOrm(
        project=project,
        task=task.task,
        description=task.description,
        priority=task.priority,
        deadline=task.deadline
    )
    session.add(new_task)
    await session.commit()
    return await get_task_by_id(session, new_task.id, customer_id)


async def get_task_by_id(session: AsyncSession, task_id: int, customer_id: int) -> TasksOrm:
    task = await session.scalar(
        select(TasksOrm)
        .where(TasksOrm.id == task_id)
        .options(
            selectinload(TasksOrm.project)
        )
    )
    if task is None:
        raise NotFoundError('Задача не найдена!')

    project = await get_project_by_id(session, task.project_id)
    if project.customer_id != customer_id:
        raise AccessDeniedError()
    return task


async def get_tasks_by_priority(session: AsyncSession, project_id: int, priority: str) -> list[TasksOrm]:
    tasks = await session.scalars(
        select(TasksOrm)
        .options(
            selectinload(TasksOrm.project)
        )
        .where(
            TasksOrm.priority == priority.value,
            TasksOrm.project_id == project_id
        )
    )

    result = tasks.all()
    if len(result) == 0:
        raise NotFoundError('Задачи не найдены!')
    return result


async def update_tasks(session: AsyncSession, task_id: int, data: UpdateTask, customer_id: int) -> TasksOrm:
    task = await get_task_by_id(session, task_id)
    project = await get_project_by_id(session, task.project_id)
    if project.customer_id != customer_id:
        raise AccessDeniedError()

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(task, key, value)

    await session.commit()
    return task


async def delete_task(session: AsyncSession, task_id: int, customer_id: int) -> dict:
    task = await get_task_by_id(session, task_id, customer_id)
    project = await get_project_by_id(session, task.project_id)
    if project.customer_id != customer_id:
        raise AccessDeniedError()

    await session.delete(task)
    await session.commit()
    return {'msg': 'Задача удалена!'}