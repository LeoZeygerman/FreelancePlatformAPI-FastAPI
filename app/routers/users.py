from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.users import UsersOrm
from app.schemas.users import CreateUser, ResponseUser


router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post('/create', summary='Добавить пользователя', response_model=ResponseUser)
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


@router.get('/get-all', summary='Показать всех пользователей')
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