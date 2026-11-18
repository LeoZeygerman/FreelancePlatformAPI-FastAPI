from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.projects import ProjectsOrm
from app.models.tasks import TasksOrm
from app.schemas.projects import CreateProject


async def create_project(session: AsyncSession, project: CreateProject):
    new_project = ProjectsOrm(
        title=project.title,
        description=project.description,
        budget=project.budget,
        customer_id=project.customer_id,
        project_task=[
            TasksOrm(
                task=task.task,
                description=task.description,
                priority=task.priority,
                deadline=task.deadline
            )
            for task in project.project_task
        ]
    )
    session.add(new_project)
    await session.commit()
    return await get_project_by_id(session, new_project.id)


async def get_project_by_id(session: AsyncSession, project_id: int):
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
    return project


async def get_all_projects(session: AsyncSession):
    projects = await session.scalars(
        select(ProjectsOrm)
    )
    result = projects.all()
    return result