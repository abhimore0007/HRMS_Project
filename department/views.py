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


def index(request):
    return render(request, 'core/index.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            try:
                user = Employe_User.objects.get(username=username)
                if not user.check_password(password):  # Manually check password
                    raise Employe_User.DoesNotExist
            except Employe_User.DoesNotExist:
                messages.error(request, "Invalid username or password!")
                return redirect("login")

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        if user.is_superuser:
            return redirect("department_dashboard")
        else:
            return redirect("/user_dashboard/")

    return render(request, "core/login.html")

def user_logout(request):
    logout(request)
    return redirect('index')

# @login_required
def user_dashboard(request):
    department_id = request.GET.get('department')
    role_id = request.GET.get('role')
    manager_id = request.GET.get('manager')

    users = Employe_User.objects.all()
    
    if department_id:
        users = users.filter(dept_id=department_id)
    if role_id:
        users = users.filter(role_id=role_id)
    if manager_id:
        users = users.filter(reporting_manager_id=manager_id)

    departments = Department.objects.all()
    roles = Role.objects.all()
    managers = Employe_User.objects.filter(role__role_name="Manager")

    return render(request, 'core/user_dashboard.html', {
        'users': users,
        'departments': departments,
        'roles': roles,
        'managers': managers
    })

# Dashboard View
def department_dashboard(request):
    if request.user.is_staff:
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
