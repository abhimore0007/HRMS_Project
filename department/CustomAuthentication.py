from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from employe.models import Employe_User  # Import your EmployeeUser model
from django.contrib.auth import login as django_login

User = get_user_model()

def custom_authenticate(username, password):
    # Check in User model
    user = User.objects.filter(username=username).first()
    if user and check_password(password, user.password):  # Verify password
        return user

    # Check in EmployeeUser model
    emp_user = Employe_User.objects.filter(username=username).first()
    if emp_user and check_password(password, emp_user.password):  # Verify password
        return emp_user

    return None  # No matching user found

def custom_login(request, username, password):
    """Custom login function that checks credentials and manually sets the session."""
    try:
        # Check in User model
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):  # Verify password
            request.session['user_id'] = user.id  # Store user id in session
            request.session['username'] = user.username
            request.session['is_superuser'] = user.is_superuser if hasattr(user, 'is_superuser') else False
            print(f"User {user.username} logged in with custom session.")
            return user

        # Check in EmployeeUser model
        emp_user = Employe_User.objects.filter(username=username).first()
        if emp_user and check_password(password, emp_user.password):  # Verify password
            request.session['user_id'] = emp_user.id  # Store user id in session
            request.session['username'] = emp_user.username
            request.session['is_superuser'] = emp_user.is_superuser if hasattr(emp_user, 'is_superuser') else False
            print(f"Employee user {emp_user.username} logged in with custom session.")
            return emp_user

        # Return None if no matching user found
        print(f"Login failed for username: {username}.")
        return None
    except Exception as e:
        print(f"Error during login: {str(e)}")  # Log the error
        return None