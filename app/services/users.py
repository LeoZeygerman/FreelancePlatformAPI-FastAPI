from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NotFoundError, UnprocessableEntityError
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.users import CreateUser, UpdateUser
from sqlalchemy.orm import selectinload
from app.services.lookups import get_user_by_id


async def get_all_users(session: AsyncSession) -> list[UsersOrm]:
    users = await session.scalars(
        select(UsersOrm)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )

    result = users.all()
    if len(result) == 0:
        raise NotFoundError('Пользователей нет!')
    return result


async def get_user_by_role(session: AsyncSession, user_id: int, role: str) -> UsersOrm:
    user = await get_user_by_id(session, user_id)
    if user.role != role:
        raise NotFoundError('У пользователя другая роль!')
    return user


async def get_user_by_rating(session: AsyncSession, limit: int, role: str, min_rating: int, max_rating: int) -> list[UsersOrm]:
    """
    Retrieve users filtered by role and rating range.

    Sort users by rating in descending order and
    limit the number of returned results.
    """
    if min_rating > max_rating:
        raise UnprocessableEntityError('Ошибка значений рейтинга!')

    users = await session.scalars(
        select(UsersOrm)
        .where(
            UsersOrm.role == role, 
            UsersOrm.rating.between(min_rating, max_rating)
        )
        .options(
            selectinload(UsersOrm.customer_projects),
            selectinload(UsersOrm.developer_projects)
        )
        .order_by(UsersOrm.rating.desc().nullslast())
        .limit(limit)
    )

    result = users.all()
    if len(result) == 0:
        raise NotFoundError('Пользователи не найдены!')
    return result


async def get_users_by_projects(session: AsyncSession, limit: int, role: str) -> list[UsersOrm]:
    """
    Retrieve users ranked by the number of completed projects.

    Filter users by role and sort them by completed
    project count in descending order.
    """
    if role == 'developer':
        users = await session.execute(
            select(
                UsersOrm.id,
                UsersOrm.username,
                UsersOrm.email,
                func.count(ProjectsOrm.developer_id).label('projects_count')
            )
            .where(
                UsersOrm.role == 'developer',
                ProjectsOrm.status == True
            )
            .group_by(UsersOrm.id)
            .join(ProjectsOrm, ProjectsOrm.developer_id == UsersOrm.id)
            .order_by(func.count(ProjectsOrm.developer_id).desc())
            .limit(limit)
        )
    elif role == 'customer':
        users = await session.execute(
            select(
                UsersOrm.id,
                UsersOrm.username,
                UsersOrm.email,
                func.count(ProjectsOrm.customer_id).label('projects_count')
            )
            .where(
                UsersOrm.role == 'customer',
                ProjectsOrm.status == True
            )
            .group_by(UsersOrm.id)
            .join(ProjectsOrm, ProjectsOrm.customer_id == UsersOrm.id)
            .order_by(func.count(ProjectsOrm.customer_id).desc())
            .limit(limit)
        )

    result = users.mappings().all()
    if len(result) == 0:
        raise NotFoundError('Пользователи не найдены!')
    return result


async def get_customers_by_cost(session: AsyncSession, limit: int) -> list[UsersOrm]:
    """
    Retrieve customers and their projects sorted by budget.

    Sort the results by project budget in descending
    order, with the most expensive projects first.
    """
    customers = await session.execute(
        select(
            UsersOrm.id,
            UsersOrm.username,
            UsersOrm.email,
            UsersOrm.rating,
            ProjectsOrm.title.label('project_title'),
            ProjectsOrm.budget.label('project_budget'),
            ProjectsOrm.status.label('project_status')
        )
        .where(UsersOrm.role == 'customer')
        .join(ProjectsOrm, ProjectsOrm.customer_id == UsersOrm.id)
        .order_by(ProjectsOrm.budget.desc())
        .limit(limit)
    )

    result = customers.mappings().all()
    if len(result) == 0:
        raise NotFoundError('Пользователи не найдены!')
    return result


async def create_user(session: AsyncSession, user: CreateUser) -> UsersOrm:
    new_user = UsersOrm(
        username = user.username,
        role = user.role,
        email = user.email
    )
    session.add(new_user)
    await session.commit()
    return await get_user_by_email(session, user.email)


async def get_user_by_email(session: AsyncSession, user_email: EmailStr) -> UsersOrm:
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == user_email)
    )

    if user is None:
        raise NotFoundError(f'Пользователь с email {user_email} не найден!')
    return user


async def update_user(session: AsyncSession, user_id: int, data: UpdateUser) -> UsersOrm:
    user = await get_user_by_id(session, user_id)
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(user, key, value)
    await session.commit()
    return await get_user_by_id(session, user_id)


async def delete_user(session: AsyncSession, user_id: int) -> dict:
    user = await get_user_by_id(session, user_id)
    await session.delete(user)
    await session.commit()
    return {'msg': f'Пользователь {user.username} удален!'}



