from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from roles.models import Role, UserRole
from employe.models import Employee



def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! You can now login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'core/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            # Check if user is an admin
            if user.is_staff:
                return redirect('department_dashboard')

            # Check if user has a role assigned
            user_role = UserRole.objects.filter(user=user).first()
            if user_role:
                return redirect('user_dashboard')
            else:
                messages.warning(request, "No role assigned. Please contact the admin.")
                return redirect('no_role_page')  # Redirects to no_role.html

        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def user_dashboard(request):
    # Check if the user has an assigned role
    user_role = UserRole.objects.filter(user=request.user).first()

    if not user_role:
        # If no role is assigned, render a page informing the user
        return render(request, 'core/no_role.html', {'message': "No role assigned. Please contact the admin."})

    # Fetch user permissions if a role exists
    user_permissions = user_role.permissions.all()
    return render(request, 'core/user_dashboard.html', {'user_role': user_role, 'user_permissions': user_permissions})

# Dashboard View
def department_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)
    return render(request, 'core/dashboard.html', {'departments': departments})

def department_details(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    roles = Role.objects.filter(department=department, status=True)  # ✅ Fetch roles for this department

    return render(request, 'core/department_detail.html', {
        'department': department,
        'roles': roles,  # ✅ Pass roles to the template
    })


# Create Department
def add_department(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')  # Redirect if the user is not staff

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # Directly save the department without checking existence
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
        department.status = False  # Soft delete
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('department_dashboard')

    return render(request, 'core/confirm_delete.html', {'department': department})


def no_role(request):
    return render(request, 'core/no_role.html', {'message': "No role assigned. Please contact the admin."})
