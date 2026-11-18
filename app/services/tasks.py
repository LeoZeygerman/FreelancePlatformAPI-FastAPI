from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.projects import ProjectsOrm
from app.models.tasks import TasksOrm
from app.schemas.tasks import CreateTask
from app.services.lookups import get_user_by_id


async def create_task(session: AsyncSession, customer_id: int, task: CreateTask):
    user = await get_user_by_id(session, customer_id)
    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == task.project_id)
    )

    new_task = TasksOrm(
        project=project,
        task=task.task,
        description=task.description,
        priority=task.priority,
        deadline=task.deadline
    )
    session.add(new_task)
    await session.commit()
    return await get_task_by_id(session, new_task.id)


async def get_task_by_id(session: AsyncSession, task_id: int):
    task = await session.scalar(
        select(TasksOrm)
        .where(TasksOrm.id == task_id)
        .options(
            selectinload(TasksOrm.project)
        )
    )
    return task


async def get_tasks_by_priority(session: AsyncSession, project_id: int, priority: str):
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
    return result