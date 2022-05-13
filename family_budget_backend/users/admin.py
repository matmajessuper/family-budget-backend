from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CreatedUpdatedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'updated')


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
