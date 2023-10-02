from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'is_active', 'is_verified', 'created_at')


admin.site.register(User, UserAdmin)