from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from employe.models import Employe_User  # Import custom user model

class EmailAuthBackend(ModelBackend):
    """Authenticate using email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Employe_User.objects.get(email=username)  # Authenticate with email
            if check_password(password, user.password):  # Verify password
                return user
        except Employe_User.DoesNotExist:
            return None
