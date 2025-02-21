from django.db import models
from employe.models import Employe_User
# Create your models here.
class Task(models.Model):
    """Task model storing task details."""
    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=100)
    task_description = models.TextField(max_length=300)
    task_priority = models.CharField(max_length=50, choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")])
    start_date = models.DateField()
    end_date = models.DateField()
    task_type = models.CharField(max_length=50, choices=[("Individual", "Individual"), ("Team", "Team")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title

class TaskAssignment(models.Model):
    """Links tasks to employees who are assigned to them."""
    assignment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE, related_name="tasks")
    assigned_by = models.ForeignKey(
        Employe_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    ) 
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed")],
        default="Pending"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_by_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.task.task_title} - {self.employee.first_name}"