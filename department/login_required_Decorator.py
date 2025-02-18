from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('login')  # Adjust 'login' with your actual login URL name
            return redirect(f"{login_url}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
