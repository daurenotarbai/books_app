from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class InvalidCode(ValidationError):
    default_detail = {
        'code': 'invalid_code',
        'message': 'Invalid code', }


class UserIsNotActive(ValidationError):
    default_detail = {
        'code': 'user_disabled',
        'message': 'User disabled', }


class EmailIsNotVerified(ValidationError):
    default_detail = {
        'code': 'email_not_verified',
        'message': 'Email is not verified',
    }


class IncorrectPassword(AuthenticationFailed):
    default_detail = {
        'code': 'email_or_password_incorrect',
        'message': 'email or password incorrect',
    }


class EmailAlreadyExist(ValidationError):
    default_detail = {
        'code': 'email_already_exist',
        'message': 'Email already exist, please login',
    }


class EasyPassword(ValidationError):
    default_detail = {
        'password': "Password must be at least 8 characters.",
        'code': "easy_password",
    }


class InvalidEmail(ValidationError):
    default_detail = {
        'email': "Email must be in English characters and contains @ symbol",
        'code': "invalid_email",
    }


class EmailNotFound(ValidationError):
    default_detail = {
        'email': "Email not found",
        'code': "email_not_found",
    }