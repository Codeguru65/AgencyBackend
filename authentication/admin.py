from django.contrib import admin

# Register your models here.
from .models import User, Institution


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'institution', 'auth_provider', 'created_at', 'is_verified']
    # exclude = ['password', ]
    readonly_fields = ('last_login',)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'agent_category', 'industry', 'email', 'agent_check', 'mobile_1']

