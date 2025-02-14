from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employe_User  # Import your custom User model

# Customizing the UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ("employee_id", "first_name", "last_name", "email", "mobile", "dept", "role", "reporting_manager", "date_of_joining")
    search_fields = ("first_name", "last_name", "email", "mobile")
    list_filter = ("dept", "role")
    fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "mobile")}),
        ("Job Details", {"fields": ("dept", "role", "reporting_manager", "date_of_joining")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        ("Create New User", {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "mobile", "dept", "role", "reporting_manager", "password1", "password2"),
        }),
    )
    ordering = ("employee_id",)
    readonly_fields = ("created_at", "updated_at")

# Register the User model with the custom admin
admin.site.register(Employe_User, CustomUserAdmin)
