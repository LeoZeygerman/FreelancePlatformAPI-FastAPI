from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import engine
from app.exceptions import AppException
from app.models.base import Base
from app.routers.tasks import router as tasks_router
from app.routers.payments import router as payments_router
from app.routers.applications import router as applications_router
from app.routers.users import router as users_router
from app.routers.projects import router as projects_router

#TODO: Документ-строки, абстракция, сложный обработчик ошибок
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppException)
async def exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def valication_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            'detail': 'Ошибка валидации данных.',
            'errors': exc.errors()
        }
    )


app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(applications_router)
app.include_router(payments_router)