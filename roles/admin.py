from django.contrib import admin
from .models import Role, UserRole

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('role_name',)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "get_role")  # Use a custom method for 'role'

    def get_role(self, obj):
        return obj.role.role_name  # Display role name instead of object reference
    get_role.short_description = "Role"  # Set column name in Django Admin

admin.site.register(UserRole, UserRoleAdmin)

