from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.users.models import Profile

# Register your models here.
@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'preferred_language',
    ]