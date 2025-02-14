from django import forms
from .models import User
from roles.models import Role


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'dept', 'role', 'reporting_manager', 'date_of_joining']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'reporting_manager': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set queryset for role field dynamically
        if 'role' in self.fields:
            self.fields['role'].queryset = Role.objects.filter(status=True)

        # Add a placeholder for reporting manager dropdown
        self.fields['reporting_manager'].queryset = User.objects.exclude(role__isnull=True)
        self.fields['reporting_manager'].widget.attrs.update({'class': 'form-control'})

        # Add 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

    
    
