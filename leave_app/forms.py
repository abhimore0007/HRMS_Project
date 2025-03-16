from django import forms
from .models import Leave

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date', 'total_days']

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['status']
