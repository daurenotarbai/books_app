from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from auth.utils import send_code_for_verify
from core.exceptions import IncorrectPassword, UserIsNotActive, EmailIsNotVerified
from users.models import User


class VerifiedEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise IncorrectPassword
        if not user.is_active:
            raise UserIsNotActive
        if not user.is_verified:
            send_code_for_verify(user)
            raise EmailIsNotVerified
        if user.check_password(password):
            return user
        else:
            raise IncorrectPassword
