from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NotFoundError, AccessDeniedError
from app.models.payments import PaymentsOrm
from app.schemas.payments import CreatePayments, UpdatePayments
from app.services.lookups import get_project_by_id


async def get_payment_by_id(session: AsyncSession, payment_id: int) -> PaymentsOrm:
    payment = await session.scalar(
        select(PaymentsOrm)
        .where(PaymentsOrm.id == payment_id)
        .options(
            selectinload(PaymentsOrm.project)
        )
    )

    if payment is None:
        raise NotFoundError('Оплата не найдена!')
    return payment


async def create_payment(session: AsyncSession, payment: CreatePayments) -> PaymentsOrm:
    project = await get_project_by_id(session, payment.project_id)

    new_payment = PaymentsOrm(
        project = project,
        amount = payment.amount
    )

    session.add(new_payment)
    await session.commit()
    return await get_payment_by_id(session, new_payment.id)


async def update_payment(session: AsyncSession, payment_id: int, data: UpdatePayments, user_id: int) -> PaymentsOrm:
    payment = await get_payment_by_id(session, payment_id)
    project = await get_project_by_id(session, payment.project_id)
    if project.customer_id != user_id:
        raise AccessDeniedError()

    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(payment, key, value)

    await session.commit()
    return await get_payment_by_id(session, payment_id)


async def delete_payment(session: AsyncSession, payment_id: int, user_id: int) -> dict:
    payment = await get_payment_by_id(session, payment_id)
    project = await get_project_by_id(session, payment.project_id)
    if project.customer_id != user_id:
        raise AccessDeniedError()

    await session.delete(payment)
    await session.commit()
    return {'msg': f'Оплата {payment_id} удалена!'}