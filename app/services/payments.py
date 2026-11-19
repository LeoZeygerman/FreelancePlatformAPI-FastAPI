from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payments import PaymentsOrm
from app.schemas.payments import CreatePayments
from app.services.lookups import get_project_by_id


async def create_payment(session: AsyncSession, payment: CreatePayments):
    project = await get_project_by_id(session, payment.project_id)

    new_payment = PaymentsOrm(
        project = project,
        amount = payment.amount
    )

    session.add(new_payment)
    await session.commit()
    return await get_payment_by_id(session, new_payment.id)