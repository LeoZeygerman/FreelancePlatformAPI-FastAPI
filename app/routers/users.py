from fastapi import APIRouter
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