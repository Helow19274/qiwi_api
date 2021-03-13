class ApiError(Exception):
    pass


class WrongToken(ApiError):
    pass


class PermissionError(ApiError):
    pass
