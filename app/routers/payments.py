from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.payments import CreatePayments, ResponsePayments, UpdatePayments
from app.services.payments import create_payment, delete_payment, get_payment_by_id, update_payment


router = APIRouter(prefix='/payment', tags=['Оплата'])


@router.post('/create', summary='Добавить оплату', response_model=ResponsePayments)
async def create_payment_router(session: SessionDep, payment: CreatePayments):
    new_payment = await create_payment(session, payment)
    return new_payment


@router.get('/{payment_id}', summary='Найти оплату по ID', response_model=ResponsePayments)
async def get_payment_router(session: SessionDep, payment_id: int):
    payment = await get_payment_by_id(session, payment_id)
    return payment


@router.patch('/update/{payment_id}', summary='Обновить оплату', response_model=ResponsePayments)
async def update_payment_router(session: SessionDep, payment_id: int, data: UpdatePayments, user_id: int):
    payment = await update_payment(session, payment_id, data, user_id)
    return payment


@router.delete('/delete/{payment_id}', summary='Удалить оплату')
async def delete_payment_router(session: SessionDep, payment_id: int, user_id: int):
    payment = await delete_payment(session, payment_id, user_id)
    return payment