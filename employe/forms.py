from django import forms
from .models import Employe_User
from roles.models import Role
from department.models import Department

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        required=True
    )

    class Meta:
        model = Employe_User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'mobile', 'dept',
            'role', 'reporting_manager', 'date_of_joining', 'password'
        ]
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

        # Set queryset for reporting manager dynamically
        self.fields['reporting_manager'].queryset = Employe_User.objects.exclude(role__isnull=True)
        self.fields['reporting_manager'].widget.attrs.update({'class': 'form-control'})

        # Add 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        """Override save method to hash password before saving the user"""
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user
