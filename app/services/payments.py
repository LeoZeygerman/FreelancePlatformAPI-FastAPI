from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.payments import CreatePayments


async def creat_payment(session: AsyncSession, payment: CreatePayments):
    pass