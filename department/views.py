from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from roles.models import Role, UserRole
from employe.models import Employe_User 
from django.urls import reverse

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from task.models import Task
from django.views.decorators.csrf import csrf_exempt
from task.models import TaskAssignment


def index(request):
    return render(request, 'core/index.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Attempting login for username: {username}")  # Debugging

        user = authenticate(request, username=username, password=password)

        if user is None:  # If authentication fails for built-in User model
            print("User not found in built-in User model, checking Employe_User...")
            try:
                user = Employe_User.objects.get(username=username)
                if not user.check_password(password):  # Check password manually
                    print("Password check failed for Employe_User.")
                    raise Employe_User.DoesNotExist
            except Employe_User.DoesNotExist:
                print("User not found in Employe_User model.")
                messages.error(request, "Invalid username or password!")
                return redirect("login")

        print(f"Login successful for user: {user.username} (Superuser: {user.is_superuser})")

        login(request, user)


        if user.is_superuser:
            print("Redirecting to department_dashboard...")
            return redirect("department_dashboard")
        else:
            print("Redirecting to user_dashboard...")
            return redirect("user_dashboard")

    return render(request, "core/login.html")

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def user_dashboard(request):
    """Dashboard displaying users and assigned tasks."""
    print("user dashboard successfull redirect") 
    user=request.user
    print(f"{user} is the user")
    department_id = request.GET.get('department')
    role_id = request.GET.get('role')
    manager_id = request.GET.get('manager')

    # Fetch users
    users = Employe_User.objects.all()
    if department_id:
        users = users.filter(dept_id=department_id)
    if role_id:
        users = users.filter(role_id=role_id)
    if manager_id:
        users = users.filter(reporting_manager_id=manager_id)

    # Fetch assigned tasks related to the logged-in user
    assigned_tasks = TaskAssignment.objects.filter(employee=request.user)

    # Fetch all departments, roles, and managers
    departments = Department.objects.all()
    roles = Role.objects.all()
    managers = Employe_User.objects.filter(role__role_name="Manager")

    return render(request, 'core/user_dashboard.html', {
        'users': users,
        'departments': departments,
        'roles': roles,
        'managers': managers,
        'assigned_tasks': assigned_tasks  # Pass tasks to the template
    })

# Dashboard View
def department_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)
    return render(request, 'core/dashboard.html', {'departments': departments})

def department_details(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    roles = Role.objects.filter(department=department, status=True)

    return render(request, 'core/department_detail.html', {
        'department': department,
        'roles': roles,
    })


# Create Department
def add_department(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('department_dashboard')
    else:
        form = DepartmentForm()

    return render(request, 'core/add_department.html', {'form': form})

# Update Department
def update_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_dashboard')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'core/update_department.html', {'form': form, 'department': department})

# Soft Delete Department (Set Status to False)
def delete_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)

    if request.method == "POST":
        department.status = False
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('department_dashboard')

    return render(request, 'core/confirm_delete.html', {'department': department})

def no_role(request):
    return render(request, 'core/no_role.html', {'message': "No role assigned. Please contact the admin."})


def Forgot_pass(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = Employe_User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                settings.EMAIL_HOST_USER, 
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('success_page')
        else:
            messages.success(request,'please enter valid email address')
    return render(request,"core/forgat_Password.html")

def success_page(request):
    return render(request, 'core/success.html')


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = Employe_User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, Employe_User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')


# ---------------------------------------------------------------------------------------------------------------------------------------------



