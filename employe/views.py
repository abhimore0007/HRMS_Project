from django.shortcuts import render, redirect, get_object_or_404
from .models import User  # Assuming your Employee model is named 'User'
from department.models import Department
from roles.models import Role
from .forms import EmployeeForm  # Ensure you have an EmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import logging

def create_employee(request):
    print("➡️ create_employee function called!")  # Debugging
    departments = Department.objects.all()  # ✅ Get all departments
    roles = Role.objects.all()  # ✅ Get all roles

    if request.method == "POST":
        print("✅ Received POST request")  # Debugging
        form = EmployeeForm(request.POST)
        if form.is_valid():
            print("✅ Form is valid")  # Debugging
            employee = form.save(commit=False)

            # ✅ Fetch department safely
            department_id = request.POST.get('dept_id')  # Make sure 'dept_id' exists in form
            print(f"🔎 department_id: {department_id}")  # Debugging
            department = Department.objects.filter(dept_id=department_id).first()
            if not department:
                messages.error(request, "❌ Invalid department selected")
                print("❌ Invalid department")  # Debugging
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            # ✅ Fetch role safely
            role_id = request.POST.get('role_id')
            print(f"🔎 role_id: {role_id}")  # Debugging
            role = Role.objects.filter(id=role_id).first()
            if not role:
                messages.error(request, "❌ Invalid role selected")
                print("❌ Invalid role")  # Debugging
                return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})

            # ✅ Assign department and role
            employee.department = department
            employee.role = role
            employee.save()
            print("✅ Employee saved successfully!")  # Debugging

            messages.success(request, "🎉 Employee created successfully!")
            return redirect('employee_list')

        else:
            print("❌ Form is not valid", form.errors)  # Debugging

    else:
        print("➡️ GET request received")  # Debugging
        form = EmployeeForm()

    return render(request, 'core/employee_form.html', {'form': form, 'departments': departments, 'roles': roles})



@login_required
@user_passes_test(lambda u: u.is_superuser or u.role.role_name == "HR")
def employee_list(request):
    employees = User.objects.select_related('dept', 'role', 'reporting_manager').all()
    return render(request, 'core/employee_list.html', {'employees': employees})



# Initialize logger
logger = logging.getLogger(__name__)

@login_required
@user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'role') and u.role.role_name == "HR"))
def update_employee(request, employee_id):
    logger.debug(f"🔍 Fetching employee with ID: {employee_id}")

    employee = get_object_or_404(User, pk=employee_id)
    departments = Department.objects.all()
    roles = Role.objects.all()
    managers = User.objects.exclude(pk=employee.pk)

    if request.method == "POST":
        logger.debug("✅ Received POST request")
        form = EmployeeForm(request.POST, instance=employee)

        logger.debug(f"📩 POST Data: {request.POST}")

        if form.is_valid():
            logger.debug("✅ Form is valid")

            # ✅ Fetch department safely using the correct field
            department = Department.objects.filter(dept_id=request.POST.get('department')).first()
            logger.debug(f"🔎 Selected Department: {department}")

            # ✅ Fetch role safely using the correct field
            role = Role.objects.filter(id=request.POST.get('role')).first()
            logger.debug(f"🔎 Selected Role: {role}")

            # ✅ Fetch manager (Optional)
            manager = User.objects.filter(pk=request.POST.get('manager_id')).first() if request.POST.get('manager_id') else None
            logger.debug(f"🔎 Selected Manager: {manager}")

            # ✅ Assign updated values
            employee = form.save(commit=False)
            employee.department = department
            employee.role = role
            employee.reporting_manager = manager
            employee.save()

            messages.success(request, "🎉 Employee updated successfully!")
            return redirect('employee_list')

        else:
            logger.error(f"❌ Form errors: {form.errors}")
            messages.error(request, "❌ Please correct the errors below.")

    else:
        logger.debug("➡️ GET request received")
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
    employee = get_object_or_404(User, employee_id=employee_id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('employee_list')

    return render(request, 'core/confirm_delete.html', {'employee': employee})