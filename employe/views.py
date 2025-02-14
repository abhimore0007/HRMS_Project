from django.shortcuts import render, redirect, get_object_or_404
from .models import Employe_User
from department.models import Department
from roles.models import Role
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def create_employee(request):
    logger.debug("create_employee function called!")

    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(status=True)

    if request.method == "POST":
        logger.debug("Received POST request")
        form = EmployeeForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            employee = form.save(commit=False)

            department_id = request.POST.get('dept_id')
            department = Department.objects.filter(dept_id=department_id, status=True).first()
            if not department:
                messages.error(request, "Invalid or inactive department selected")
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            role_id = request.POST.get('role_id')
            role = Role.objects.filter(id=role_id, status=True).first()
            if not role:
                messages.error(request, "Invalid or inactive role selected")
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            employee.department = department
            employee.role = role
            employee.save()
            messages.success(request, "Employee created successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role.role_name == "HR")
def employee_list(request):
    employees = Employe_User.objects.select_related('dept', 'role', 'reporting_manager').all()
    return render(request, 'core/employee_list.html', {'employees': employees})


@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'role') and u.role.role_name == "HR"))
def update_employee(request, employee_id):
    logger.debug(f"Fetching employee with ID: {employee_id}")

    employee = get_object_or_404(Employe_User, pk=employee_id)
    departments = Department.objects.filter(status=True)
    roles = Role.objects.filter(status=True)
    managers = Employe_User.objects.exclude(pk=employee.pk)

    if request.method == "POST":
        logger.debug("Received POST request")
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            logger.debug("Form is valid")
            department_id = request.POST.get('department')
            department = Department.objects.filter(dept_id=department_id, status=True).first()
            role_id = request.POST.get('role')
            role = Role.objects.filter(id=role_id, status=True).first() or Role.objects.create(role_name="N/A", status=True)
            manager_id = request.POST.get('manager_id')
            manager = Employe_User.objects.filter(pk=manager_id).first() if manager_id else None

            employee = form.save(commit=False)
            employee.department = department
            employee.role = role
            employee.reporting_manager = manager
            employee.save()

            messages.success(request, "Employee updated successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'core/update_employe.html', {
        'form': form, 
        'departments': departments, 
        'roles': roles, 
        'managers': managers, 
        'employee': employee
    })


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role.role_name == "HR")
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employe_User, employee_id=employee_id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('employee_list')

    return render(request, 'core/confirm_delete.html', {'employee': employee})
