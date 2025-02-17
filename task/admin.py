from django.contrib import admin
from .models import Task, TaskAssignment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'task_priority', 'start_date', 'end_date', 'task_type', 'created_at', 'updated_at')
    search_fields = ('task_title', 'task_priority', 'task_type')
    list_filter = ('task_priority', 'task_type', 'start_date', 'end_date')

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'employee', 'assigned_by', 'assigned_date', 'status', 'completed_at')
    search_fields = ('task__task_title', 'employee__first_name', 'assigned_by__first_name', 'status')
    list_filter = ('status', 'assigned_date', 'completed_at')
