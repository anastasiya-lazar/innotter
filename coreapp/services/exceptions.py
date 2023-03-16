from rest_framework.exceptions import APIException


class RefreshTokenException(APIException):
    status_code = 401
    default_detail = "Invalid Refresh Token."


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Invalid Credentials. Try again."


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = "User not found."


class InvalidPageException(APIException):
    status_code = 400
    default_detail = "Invalid page."
