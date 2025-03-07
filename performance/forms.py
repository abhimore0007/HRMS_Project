from django import forms
from .models import PerformanceReview
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the User model

class PerformanceReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), str(i)) for i in range(1, 11)]  # Generates choices from 1 to 10

    class Meta:
        model = PerformanceReview
        fields = ['review_title', 'employee', 'reviewed_by', 'review_period', 'rating', 'comments']
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter review title'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'review_period': forms.Select(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annual', 'Annual')],
                                          attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter comments'}),
        }

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}), 
        label="Rating (1-10)"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Fetch logged-in user
        super().__init__(*args, **kwargs)

        self.fields['reviewed_by'].widget.attrs.update({'class': 'form-select'})  # Add Bootstrap styling

        if user:
            if user.is_staff or user.is_superuser:  
                # If the logged-in user is admin or staff, restrict reviewed_by field
                self.fields['reviewed_by'].queryset = User.objects.filter(id=user.id)
                self.fields['reviewed_by'].initial = user
                self.fields['reviewed_by'].widget.attrs['readonly'] = True  # Make it readonly
                self.fields['reviewed_by'].widget.attrs['class'] += ' form-control-plaintext'  # Display as plain text
            else:
                # If not admin/staff, remove 'reviewed_by' field (prevents them from setting it)
                self.fields.pop('reviewed_by', None)
