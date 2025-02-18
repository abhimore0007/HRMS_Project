from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employe_User  # Import your custom User model

# Customizing the UserAdmin
class CustomUserAdmin(admin.ModelAdmin):
    # Update `ordering` to use a valid field, such as `username` or `email`
    ordering = ['username']  # Or any other valid field like 'first_name', 'last_name'

    # Update `list_display` to use valid fields from the `Employe_User` model
    list_display = ('username', 'first_name', 'last_name', 'email', 'mobile', 'dept', 'role')

    # Other options for CustomUserAdmin if necessary
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
    list_filter = ('role', 'dept')  # Optional filters if needed

# Register the custom admin
admin.site.register(Employe_User, CustomUserAdmin)
