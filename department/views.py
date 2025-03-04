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
from .CustomAuthentication import custom_authenticate,custom_login
from .login_required_Decorator import custom_login_required

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

User = get_user_model()  # Get custom user model


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Fetch email correctly
        password = request.POST.get("password")

        if not email:
            print("❌ Email is None or empty")
            messages.error(request, "Email field is required")
            return render(request, "core/login.html")

        user = custom_authenticate(email=email, password=password)  # Authenticate using email

        if user is not None:
            login(request, user)
            print(f"✅ User Authenticated: {user.email}")

            if user.is_superuser:
                return redirect("department_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            print("❌ Authentication Failed")
            messages.error(request, "Invalid email or password")

    return render(request, "core/login.html")

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def user_dashboard(request):
    """Dashboard displaying users, assigned tasks, roles, and departments."""
    user = request.user
    employee = get_object_or_404(Employe_User, username=user.username)

    roles = Role.objects.all()
    departments = Department.objects.all()
    
    # Fetch tasks assigned to the logged-in employee
    assigned_tasks = TaskAssignment.objects.filter(employee=employee).select_related("task")

    print(f"User Dashboard successful redirect for {user}")

    return render(request, 'core/user_dashboard.html', {
        "user": user,
        "roles": roles,
        "departments": departments,
        "assigned_tasks": assigned_tasks
    })

# Dashboard View
def department_dashboard(request):
    user=request.user
    print(f"{user} is user")
    if not request.user.is_superuser:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)

    department_data = []
    for dept in departments:
        active_employees = Employe_User.objects.filter(dept=dept, is_active=True).count()
        inactive_employees = Employe_User.objects.filter(dept=dept, is_active=False).count()
        department_data.append({
            'department': dept,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees
        })

    return render(request, 'core/dashboard.html', {
        'department_data': department_data,
        'departments': departments  # Added this line
    })

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


@login_required
def update_task_status(request, assignment_id):
    """Handles task status updates."""
    if request.method == "POST":
        task_assignment = get_object_or_404(TaskAssignment, assignment_id=assignment_id)
        new_status = request.POST.get("status")
        task_assignment.status = new_status
        task_assignment.save()
        messages.success(request, "Task status updated successfully!")
    
    return redirect('user_dashboard')


# ---------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def profile_view(request):
    user = request.user
    first_name = user.first_name
    last_name = user.last_name

    initials = ""
    if first_name and last_name:
        initials = f"{first_name[0]}{last_name[0]}"
    elif first_name:
        initials = first_name[0]
    elif last_name:
        initials = last_name[0]

    return render(request, 'core/profile.html', {'initials': initials})

def all_section(request):
    return render(request,'core/all_section.html')
