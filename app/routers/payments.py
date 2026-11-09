from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.models.payments import PaymentsOrm
from app.models.projects import ProjectsOrm
from app.schemas.payments import CreatePayments, ResponsePayments


router = APIRouter(prefix='/payment', tags=['Оплата'])


@router.post('/create', summary='Добавить оплату', response_model=ResponsePayments)
async def create_payment_router(session: SessionDep, payment: CreatePayments):
    project = await session.scalar(
        select(ProjectsOrm)
        .where(ProjectsOrm.id == payment.project_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')

    new_payment = PaymentsOrm(
        project = project,
        amount = payment.amount
    )

    session.add(new_payment)
    await session.flush()
    await session.commit()
    return new_payment


@router.get('/{payment_id}', summary='Найти оплату по ID', response_model=ResponsePayments)
async def get_payment_router(session: SessionDep, payment_id: int):
    payment = await session.scalar(
        select(PaymentsOrm)
        .where(PaymentsOrm.id == payment_id)
        .options(
            selectinload(PaymentsOrm.project)
        )
    )
    if payment is None:
        raise HTTPException(status_code=404, detail='Оплата не найдена!')

    return payment