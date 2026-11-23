class AppException(Exception):
    status_code = 500
    detail = 'Ошибка сервера!'

    def __init__(self, detail: str | None = None):
        self.detail = (
            detail if detail is not None
            else self.detail
        )


class NotFoundError(AppException):
    status_code = 404
    detail = 'Объект не найден!'


class AccessDeniedError(AppException):
    status_code = 403
    detail = 'Недостаточно прав!'


class UnprocessableEntityError(AppException):
    status_code = 422
    detail = 'Ошибка в значениях!'