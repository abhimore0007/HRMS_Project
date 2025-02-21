from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from employe.models import Employe_User  # Import your EmployeeUser model
from django.contrib.auth import login as django_login
from django.utils.crypto import constant_time_compare
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string
from django.views.decorators.debug import sensitive_variables
from django.conf import settings
from django.contrib.auth import login

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

SESSION_KEY = "_auth_user_id"
BACKEND_SESSION_KEY = "_auth_user_backend"
HASH_SESSION_KEY = "_auth_user_hash"


User = get_user_model()

def load_backend(path):
    return import_string(path)()


def _get_backends(return_tuples=False):
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            "No authentication backends have been defined. Does "
            "AUTHENTICATION_BACKENDS contain anything?"
        )
    return backends



def custom_authenticate(email, password):
    email = email.strip()  # Remove any accidental spaces
    emp_user = Employe_User.objects.filter(email=email).first()
    print(f"User found: {emp_user}")  # Confirm if user is retrieved

    if not emp_user:
        print("❌ No user found with this email")
        return None  # User doesn't exist

    if not check_password(password, emp_user.password):
        print("❌ Password mismatch")
        return None  # Password incorrect

    return emp_user  # Return authenticated user
  # No matching user found


"""
def login(request, user, backend=None):
    
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    
    session_auth_hash = ""
    if user is None:
        user = request.user
    if hasattr(user, "get_session_auth_hash"):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
            session_auth_hash
            and not constant_time_compare(
                request.session.get(HASH_SESSION_KEY, ""), session_auth_hash
            )
        ):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                "You have multiple authentication backends configured and "
                "therefore must provide the `backend` argument or set the "
                "`backend` attribute on the user."
            )
    else:
        if not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, "user"):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)

"""


def custom_login(request, username, password):
    """Custom login function that checks credentials and manually sets the session."""
    try:
        # Check in User model
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):  # Verify password
            login(request, user)  # Django's built-in login
            request.session['is_superuser'] = user.is_superuser if hasattr(user, 'is_superuser') else False
            print(f"User {user.username} logged in successfully.")
            return user  # Return authenticated user

        # Check in EmployeeUser model
        emp_user = Employe_User.objects.filter(username=username).first()
        if emp_user and check_password(password, emp_user.password):
            login(request, emp_user)  # Login the EmployeeUser
            request.session['is_superuser'] = emp_user.is_superuser if hasattr(emp_user, 'is_superuser') else False
            print(f"Employee User {emp_user.username} logged in successfully.")
            return emp_user  # Return authenticated EmployeeUser

        # If no user found
        print(f"Login failed for username: {username}.")
        return None

    except Exception as e:
        print(f"Error during login: {str(e)}")  # Log the error
        return None
    










    