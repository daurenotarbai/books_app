from django.db import models

from core.models import TimestampMixin
from users.models import User


# Create your models here.
class VerificationCode(TimestampMixin):

    code = models.CharField(verbose_name='Код', max_length=6)
    email = models.EmailField(verbose_name='email')
