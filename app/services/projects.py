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