from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskAssignment
from .forms import TaskForm, TaskAssignmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def task_list(request):
    """Display tasks with filtering options."""
    tasks = Task.objects.all()
    return render(request, 'core/task_list.html', {'tasks': tasks})


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form})

def assign_task(request):
    """Assign a task to an employee."""
    if not request.user.is_superuser and not request.user.groups.filter(name__in=['HR', 'Manager']).exists():
        messages.error(request, "You do not have permission to assign tasks.")
        return redirect('task_list')
    
    if request.method == "POST":
        form = TaskAssignmentForm(request.POST, request=request)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            messages.success(request, "Task assigned successfully!")
            return redirect('task_list')
    else:
        form = TaskAssignmentForm(request=request)
    return render(request, 'core/task_assignment.html', {'form': form})

@login_required
def edit_task(request, task_id):
    """Edit task details."""
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_superuser and not request.user.groups.filter(name__in=['HR', 'Manager']).exists():
        messages.error(request, "You do not have permission to edit tasks.")
        return redirect('task_list')
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id)
    if not request.user.is_superuser and not request.user.groups.filter(name__in=['HR', 'Manager']).exists():
        messages.error(request, "You do not have permission to delete tasks.")
        return redirect('task_list')
    
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('task_list')
    return render(request, 'core/task_confirm_delete.html', {'task': task})
