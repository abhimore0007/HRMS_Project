from django.contrib import admin
from .models import Role, UserRole

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('role_name',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    filter_horizontal = ('permissions',)
