from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskAssignment
from .forms import TaskForm, TaskAssignmentForm
from django.contrib.auth.models import User
from django.utils import timezone
from employe.models import Employe_User



def task_list(request):
    user=request.user
    print(f"user dashboard successfull redirect {user}")
    """Fetches all tasks and assigned tasks for display."""
    tasks = Task.objects.all()  # Fetch all tasks
    assigned_tasks = TaskAssignment.objects.all()  # Fetch all assigned tasks

    return render(request, 'core/task_list.html', {
        'tasks': tasks,
        'assigned_tasks': assigned_tasks
    })



def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            print("✅ New Task Created:", task.task_id)  # Debugging Task ID
            return redirect('task_list')
        else:
            print("❌ Form Errors:", form.errors)  # Debugging Form Errors
    else:
        form = TaskForm()

    return render(request, 'core/task_form.html', {'form': form})




def task_update(request, task_id):
    """Allows the admin to update a task."""
    task = get_object_or_404(Task, pk=task_id)

    if not request.user.is_staff:
        return redirect('task_list')

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)
    
    return render(request, 'core/task_form.html', {'form': form})


@login_required
def task_delete(request, task_id):
    """Allows the admin to delete a task."""
    task = get_object_or_404(Task, pk=task_id)

    if not request.user.is_staff:
        return redirect('task_list')

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'core/task_confirm_delete.html', {'task': task})




def assign_task(request):
    """View for assigning tasks to employees."""
    print(f"User: {request.user}, Superuser: {request.user.is_superuser}, Role: {getattr(request.user, 'role', 'No role')} - Trying to assign a task")


    if request.method == "POST":
        print("Received POST request for task assignment")
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            task_assignment = form.save(commit=False)

            if request.user.is_superuser:
                task_assignment.assigned_by = None  # Set NULL since admin is not in Employe_User
                task_assignment.assigned_by_name = request.user.username  # Store admin's username
                print(f"Task assigned by Admin: {request.user.username}")
            else:
                try:
                    employe_user = Employe_User.objects.get(username=request.user.username)
                    task_assignment.assigned_by = employe_user
                    task_assignment.assigned_by_name = f"{employe_user.first_name} {employe_user.last_name}"
                    print(f"Task assigned by Employee: {task_assignment.assigned_by_name}")
                except Employe_User.DoesNotExist:
                    print("Error: No matching Employe_User found for this user.")
                    return redirect("task_list")

            task_assignment.save()
            print("Task assigned successfully!")
            return redirect("task_list")  # Redirect to task list page
        else:
            print("Form validation failed.")
    else:
        print("Rendering empty task assignment form.")
        form = TaskAssignmentForm()

    return render(request, "core/task_assign.html", {"form": form})



# def update_task_status(request, assignment_id):
#     """Allows assigned employees, managers, and superusers to update task status."""
#     assignment = get_object_or_404(TaskAssignment, pk=assignment_id)

#     if request.user != assignment.employee and not request.user.is_superuser and getattr(request.user, 'role', '') != "manager":
#         return redirect('task_list')

#     if request.method == "POST":
#         form = TaskAssignmentForm(request.POST, instance=assignment)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#     else:
#         form = TaskAssignmentForm(instance=assignment)

#     return render(request, 'core/update_task_status.html', {'form': form})
