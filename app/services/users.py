from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UsersOrm
from app.schemas.users import CreateUser


async def create_user(session: AsyncSession, user: CreateUser):
    new_user = UsersOrm(
        username = user.username,
        role = user.role,
        email = user.email
    )
    session.add(new_user)
    await session.commit()
    