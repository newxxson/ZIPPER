from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
class CustomUserAdmin(admin.ModelAdmin):    
    model = CustomUser
    ordering = ('id',)
    list_display = ('id', 'email', 'nickname', 'age', 'sex', 'major')

admin.site.register(CustomUser, CustomUserAdmin)