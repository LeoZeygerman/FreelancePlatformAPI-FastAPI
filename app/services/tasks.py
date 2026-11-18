from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
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
    return await 