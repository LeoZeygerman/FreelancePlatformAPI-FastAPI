class AppException(Exception):
    status_code = 500
    detail = 'Ошибка сервера!'

    def __init__(self, detail: str | None):
        if detail:
            self.detail = detail