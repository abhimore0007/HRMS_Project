# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Role, UserRole
from .forms import RoleForm, UserRoleForm

def is_admin(user):
    return user.is_superuser  # Only allow admins to manage roles

@login_required
@user_passes_test(is_admin)
def role_list(request):
    active_roles = Role.objects.filter(status=True)
    inactive_roles = Role.objects.filter(status=False)
    return render(request, 'core/role_list.html', {'active_roles': active_roles, 'inactive_roles': inactive_roles})

@login_required
@user_passes_test(is_admin)
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'core/role_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'core/role_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    role.status = False  # Soft delete
    role.save()
    return redirect('role_list')

@login_required
@user_passes_test(is_admin)
def assign_role(request):
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = UserRoleForm()
    return render(request, 'core/Assign_role.html', {'form': form})

@login_required
def user_dashboard(request):
    user_role = get_object_or_404(UserRole, user=request.user)
    user_permissions = user_role.permissions.all()
    return render(request, 'core/user_dashboard.html', {'user_role': user_role, 'user_permissions': user_permissions})

def activate_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.status = True  # Activate the role
    role.save()
    return redirect('role_list') 
