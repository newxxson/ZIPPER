from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VerificationToken


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    ordering = ("id",)
    list_display = ("id", "email", "nickname", "student_number", "sex", "department")


admin.site.register(CustomUser, CustomUserAdmin)


class VerificationTokenAdmin(admin.ModelAdmin):
    model = VerificationToken
    ordering = "email"
    list_display = ("email", "token", "verification_type" "used")
