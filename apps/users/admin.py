from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest

from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = (
        "id",
    )