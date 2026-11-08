from fastapi import APIRouter
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