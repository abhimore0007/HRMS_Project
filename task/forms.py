from django import forms
from .models import Task, TaskAssignment

class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'task_title': forms.TextInput(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'task_priority': forms.Select(attrs={'class': 'form-control'}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
        }

class TaskAssignmentForm(forms.ModelForm):
    """Form for assigning tasks to employees."""
    
    class Meta:
        model = TaskAssignment
        fields = ['task', 'employee']  # Removed 'status' from fields for admin
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

