from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NotFoundError, AccessDeniedError
from app.models.applications import ApplicationsOrm
from app.models.projects import ProjectsOrm
from app.models.reviews import ReviewsOrm
from app.models.tasks import TasksOrm
from app.services.lookups import get_project_by_id, get_user_by_id
from app.schemas.projects import CreateProject, UpdateProject
from app.schemas.reviews import CreateReview


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
    return await get_project_with_relations(session, new_project.id)


async def get_project_with_relations(session: AsyncSession, project_id: int):
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
        raise NotFoundError(f'Проекты не найдены!')
    return project


async def get_all_projects(session: AsyncSession):
    projects = await session.scalars(
        select(ProjectsOrm)
    )

    result = projects.all()
    if len(result) == 0:
        raise NotFoundError('Проекты не найдены!')
    return result


async def get_best_paid_projects(session: AsyncSession, limit: int):
    projects = await session.scalars(
        select(ProjectsOrm)
        .order_by(ProjectsOrm.budget.desc())
        .limit(limit)
    )

    result = projects.all()
    if len(result) == 0:
        raise NotFoundError('Проекты не найдены!')
    return result


async def get_projects_by_applications(session: AsyncSession, limit: int):
    projects = await session.execute(
        select(
            ProjectsOrm.id.label('project_id'),
            ProjectsOrm.title.label('project_title'),
            func.count(ApplicationsOrm.id).label('applications')
        )
        .outerjoin(ApplicationsOrm, ApplicationsOrm.project_id == ProjectsOrm.id)
        .group_by(ProjectsOrm.id)
        .order_by(func.count(ApplicationsOrm.id).desc())
        .limit(limit)
    )

    result = projects.mappings().all()
    if len(result) == 0:
        raise NotFoundError('Проекты не найдены!')
    return result


async def update_project(session: AsyncSession, project_id: int, data: UpdateProject, user_id: int):
    project = await get_project_with_relations(session, project_id)
    if project is None:
        raise NotFoundError('Проект не найден!')
    elif project.customer_id != user_id:
        raise AccessDeniedError()

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(project, key, value)
    return await get_project_with_relations(session, project.id)


async def add_mark(session: AsyncSession, review: CreateReview, project_id: int):
    project = await get_project_by_id(session, project_id)
    if project is None:
        raise NotFoundError('Проект не найден!')

    new_mark = ReviewsOrm(
        project_id=project_id,
        reviewer_id=review.reviewer_id,
        reviewee_id=review.reviewee_id,
        rating=review.rating
    )
    session.add(new_mark)
    await session.flush()

    update_rating = await session.scalar(
        select(func.avg(ReviewsOrm.rating))
        .where(ReviewsOrm.reviewee_id == review.reviewee_id)
    )

    user = await get_user_by_id(session, review.reviewee_id)
    user.rating = update_rating

    await session.commit()
    return {'msg': f'Оценка пользователю {user.username} успешно выставлена!'}


async def delete_project(session: AsyncSession, project_id: int, user_id: int):
    project = await get_project_with_relations(session, project_id)
    if project is None:
        raise NotFoundError('Проект не найден!')
    elif project.customer_id != user_id:
        raise AccessDeniedError()

    await session.delete(project)
    await session.commit()
    return {'msg': f'Проект {project.title} удален!'}