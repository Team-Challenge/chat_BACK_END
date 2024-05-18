from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    detail = None
    status_code = None
    description = None

    def __init__(self, **kwargs):
        self.detail = kwargs.get("detail", self.detail)
        self.status_code = kwargs.get("code", self.status_code)

    @classmethod
    def desc(cls):
        return {
            "description": cls.description,
            "content": {"application/json": {"example": {"detail": cls.detail}}}
        }


class BadRequest(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad Request"
    description = "Something went wrong"


class Unauthorized(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong email or password"
    description = "Something went wrong"


class NotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"
    description = "Something not found"


class CredentialsException(BaseHTTPException):

    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status_code", status.HTTP_401_UNAUTHORIZED)
        self.detail = kwargs.get("detail", "Not found")
        self.headers = kwargs.get("headers", {"WWW-Authenticate": "Bearer"})


class TokenExpired(BaseHTTPException):
    detail = "Token is expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class IncorrectTokenFormat(BaseHTTPException):
    def __init__(self, **kwargs):
        self.detail = kwargs.get("detail", "Wrong token format")
        self.status_code = kwargs.get("code", status.HTTP_401_UNAUTHORIZED)


class UserIsNotPresent(BaseHTTPException):
    def __init__(self, **kwargs):
        self.detail = kwargs.get("detail", "User not found")
        self.status_code = kwargs.get("code", status.HTTP_401_UNAUTHORIZED)


class InternalServerError(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error. Please contact system administrator"


class ChatCreationError(BaseHTTPException):
    detail = "Shop owner cannot create chat with self"
    status_code = status.HTTP_400_BAD_REQUEST
    description = "The store owner ID and the customer ID are identical"
