from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4

from core.models import TimestampMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
          Creates a custom user with the given fields
        """
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampMixin):
    uuid = models.CharField(max_length=300, default=uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)

    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
