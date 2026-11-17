from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.projects import ProjectsOrm
from app.models.reviews import ReviewsOrm
from app.models.users import UsersOrm
from app.schemas.users import CreateUser
from sqlalchemy.orm import selectinload
from app.services.lookups import get_user_by_id

#TODO сделать оброботчик ошибок и типизацию

async def create_user(session: AsyncSession, user: CreateUser):
    new_user = UsersOrm(
        username = user.username,
        role = user.role,
        email = user.email
    )
    session.add(new_user)
    await session.commit()
    return await get_user_by_email(session, user.email)


async def get_user_by_email(session: AsyncSession, user_email: EmailStr):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.email == user_email)
    )
    return user


async def get_all_users(session: AsyncSession):
    users = await session.scalars(
        select(UsersOrm)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    result = users.all()
    return result


async def get_user_by_id(session: AsyncSession, user_id: int):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    return user


async def get_user_by_rating(session: AsyncSession, limit: int, role: str):
    users = await session.execute(
        select(UsersOrm)
        .where(UsersOrm.role == role)
        .options(
            selectinload(UsersOrm.customer_projects),
            selectinload(UsersOrm.developer_projects)
        )
        .order_by(UsersOrm.rating.desc().nullslast())
        .limit(limit)
    )
    result = users.mappings().all()
    return result


async def get_users_by_projects(session: AsyncSession, limit: int, role: str):
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
    return result


async def get_developers_by_reviews(session: AsyncSession, min_rating: int, max_rating: int, limit: int):
    #TODO сделать проверку рейтинга
    developers = await session.execute(
        select(
            UsersOrm.id,
            UsersOrm.username,
            UsersOrm.email,
            func.count(ReviewsOrm.reviewee_id).label('projects_count')
        )
        .where(
            UsersOrm.role == 'developer',
            UsersOrm.rating.between(min_rating, max_rating)
        )
        .join(ReviewsOrm, ReviewsOrm.reviewee_id == UsersOrm.id)
        .group_by(UsersOrm.id)
        .order_by(func.count(ReviewsOrm.reviewee_id).desc())
        .limit(limit)
    )
    result = developers.mappings().all()
    return result


async def get_customers_by_cost(session: AsyncSession, limit: int):
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
    )



