from django import forms
from .models import Task, TaskAssignment
from employe.models import Employe_User  # Importing Employee User Model

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_priority', 'start_date', 'end_date', 'task_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = ['task', 'assigned_to', 'status']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get logged-in user
        super().__init__(*args, **kwargs)

        if self.request:
            self.fields['assigned_to'].queryset = Employe_User.objects.filter(reports_to=self.request.user)
