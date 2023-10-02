from django.db import models


class NoAddMixin:
    def has_add_permission(self, request, obj=None):
        return False


class NoChangeMixin:
    def has_change_permission(self, request, obj=None):
        return False


class NoDeleteMixin:
    def has_delete_permission(self, request, obj=None):
        return False


class NoEditMixin(NoAddMixin, NoChangeMixin, NoDeleteMixin):
    ...


class TimestampMixin(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField("Дата изменения", auto_now=True, db_index=True)

    class Meta:
        abstract = True
