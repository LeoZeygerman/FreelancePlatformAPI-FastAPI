from fastapi import APIRouter, Query
from app.database import SessionDep
from app.schemas.users import CreateUser, ResponseCustomerWithProjects, ResponseDeveloperStats, ResponseUser, ResponseUserShort, UpdateUser
from app.services.users import create_user, delete_user, get_all_users, get_customers_by_cost, get_user_by_rating, get_user_by_role, get_users_by_projects, update_user


router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post('/create', summary='Добавить пользователя', response_model=ResponseUserShort)
async def create_user_router(session: SessionDep, user: CreateUser):
    new_user = await create_user(session, user)
    return new_user


@router.get('/get-all', summary='Показать всех пользователей', response_model=list[ResponseUser])
async def get_all_users_router(session: SessionDep):
    users = await get_all_users(session)
    return users


@router.get('/developer/{user_id}', summary='Получить разработчика по ID', response_model=ResponseUser)
async def get_developer_router(session: SessionDep, user_id: int, role='developer'):
    developer = await get_user_by_role(session, user_id, role)
    return developer


@router.get('/customer/{user_id}', summary='Получить работодателя по ID', response_model=ResponseUser)
async def get_customer_router(session: SessionDep, user_id: int, role='customer'):
    customer = await get_user_by_role(session, user_id, role)
    return customer


@router.get('/developers/most-projects', summary='Получить разработчиков по количеству выполненных проектов', response_model=list[ResponseDeveloperStats])
async def get_developers_by_projects_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100), role='developer'):
    developers = await get_users_by_projects(session, limit, role)
    return developers


@router.get('/developers/by-rating', summary='Получить разработчиков по рейтингу', response_model=list[ResponseDeveloperStats])
async def get_developers_by_rating_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100), role='developer', min_rating: int=Query(ge=1, le=5), max_rating: int=Query(ge=1, le=5),):
    developers = get_user_by_rating(session, limit, role, min_rating, max_rating)
    return developers


@router.get('/customers', summary='Получить создателей по рейтингу', response_model=list[ResponseUserShort])
async def get_top_customers_router(session: SessionDep, limit: int = Query(ge=1, default=10, le=100), role='customer', min_rating: int=Query(ge=1, le=5), max_rating: int=Query(ge=1, le=5)):
    customers = await get_user_by_rating(session, limit, role, min_rating, max_rating)
    return customers


@router.get('/customers/by-cost', summary='Получить создателей с самыми дорогостоящими проектами', response_model=list[ResponseCustomerWithProjects])
async def get_customers_by_cost_router(session: SessionDep, limit: int=Query(ge=1, default=10, le=100)):
    customers = get_customers_by_cost(session, limit)
    return customers


@router.patch('/update/{user_id}', summary='Изменить пользователя', response_model=ResponseUser)
async def update_user_router(session: SessionDep, user_id: int, data: UpdateUser):
    user = await update_user(session, user_id, data)
    return user


@router.delete('/delete/{user_id}', summary='Удалить пользователя')
async def delete_user_router(session: SessionDep, user_id: int):
    user = await delete_user(session, user_id)
    return user