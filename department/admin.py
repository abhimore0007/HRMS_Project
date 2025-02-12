from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'description', 'status', 'created_at', 'updated_at')
    search_fields = ('dept_name',)
    list_filter = ('status',)
    ordering = ('created_at',)

