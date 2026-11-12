from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.projects import ProjectsOrm
from app.models.users import UsersOrm
from app.schemas.users import CreateUser, ResponseDeveloperStats, ResponseUser, ResponseUserShort, UpdateUser
from app.models.reviews import ReviewsOrm


router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post('/create', summary='Добавить пользователя', response_model=ResponseUserShort)
async def create_user_router(session: SessionDep, user: CreateUser):
    new_user = UsersOrm(
        username = user.username,
        role = user.role,
        email = user.email
    )
    session.add(new_user)
    await session.flush()
    await session.commit()
    return new_user


@router.get('/get-all', summary='Показать всех пользователей', response_model=list[ResponseUser])
async def get_all_users_router(session: SessionDep):
    users = await session.scalars(
        select(UsersOrm)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    result = users.all()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail='Пользователи не найдены!')
    return result


@router.get('/developer/{user_id}', summary='Получить разработчика по ID', response_model=ResponseUser)
async def get_developer_router(session: SessionDep, user_id: int):
    developer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    if developer is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    elif developer.role != 'developer':
        raise HTTPException(status_code=404, detail='Пользователь не разработчик!')
    return developer


@router.get('/customer/{user_id}', summary='Получить работодателя по ID', response_model=ResponseUser)
async def get_customer_router(session: SessionDep, user_id: int):
    customer = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.customer_projects),
            selectinload(UsersOrm.developer_projects)
        )
    )
    if customer is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    elif customer.role != 'customer':
        raise HTTPException(status_code=404, detail='Пользователь не работодатель!')
    return customer


@router.get('/developers', summary='Получить топ разработчиков по рейтингу', response_model=list[ResponseUser])
async def get_top_developers_router(session: SessionDep, limit: int = Query(ge=1, default=10, le=100)):
    developers = await session.scalars(
        select(UsersOrm)
        .where(UsersOrm.role == 'developer')
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects),
        )
        .order_by(UsersOrm.rating.desc().nullslast())
        .limit(limit)
    )
    result = developers.all()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail='Разработчиков нет!')
    return result


@router.get('/developers', summary='Получить разработчиков по количеству выполненных проектов', response_model=list[ResponseDeveloperStats])
async def get_developers_by_projects_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100)):
    query = (
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
    developers = (await session.execute(query)).mappings().all()
    if len(developers) == 0:
        raise HTTPException(status_code=404, detail='Разработчиков нет!')
    return developers


@router.get('/customers', summary='Получить топ создателей по рейтингу', response_model=list[ResponseUser])
async def get_top_customers_router(session: SessionDep, limit: int = Query(ge=1, default=10, le=100)):
    customers = await session.scalars(
        select(UsersOrm)
        .where(UsersOrm.role == 'customer')
        .options(
            selectinload(UsersOrm.customer_projects),
            selectinload(UsersOrm.developer_projects)
        )
        .order_by(UsersOrm.rating.desc().nullslast())
        .limit(limit)
    )
    result = customers.all()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail='Создателей нет!')
    return result


@router.patch('/update/{user_id}', summary='Изменить пользователя', response_model=ResponseUser)
async def update_user_router(session: SessionDep, user_id: int, data: UpdateUser):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(user, key, value)

    await session.flush()
    await session.commit()
    return user


@router.delete('/delete/{user_id}', summary='Удалить пользователя')
async def delete_user_router(session: SessionDep, user_id: int):
    user = await session.scalar(
        select(UsersOrm)
        .where(UsersOrm.id == user_id)
        .options(
            selectinload(UsersOrm.developer_projects),
            selectinload(UsersOrm.customer_projects)
        )
    )
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    await session.delete(user)
    await session.commit()
    return {'msg': f'Пользователь {user.username} удален!'}