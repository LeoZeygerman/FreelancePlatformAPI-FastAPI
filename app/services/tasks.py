from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tasks import CreateTask


async def create_task(session: AsyncSession, customer_id: int, task: CreateTask):
    pass