from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payments import PaymentsOrm
from app.schemas.payments import CreatePayments, UpdatePayments
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


async def get_payment_by_id(session: AsyncSession, payment_id: int):
    payment = await session.scalar(
        select(PaymentsOrm)
        .where(PaymentsOrm.id == payment_id)
        .options(
            selectinload(PaymentsOrm.project)
        )
    )
    return payment


async def update_payment(session: AsyncSession, payment_id: int, data: UpdatePayments):
    payment = await get_payment_by_id(session, payment_id)

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(payment, key, value)

    await session.commit()
    return await get_payment_by_id(session, payment_id)