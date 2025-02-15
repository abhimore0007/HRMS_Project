from django.db import models
from employe.models import Employe_User  # Importing existing Employe_User model

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Team', 'Team'),
    ]

    task_title = models.CharField(max_length=100)
    task_description = models.TextField(max_length=300, blank=True, null=True)
    task_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    start_date = models.DateField()
    end_date = models.DateField()
    task_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Individual')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title


class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey(Employe_User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(Employe_User, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned')
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Allow only Admin, Manager, or Team Leader to assign tasks."""
        if self.assigned_by and self.assigned_by.role in ['Admin', 'Manager', 'Team Leader']:
            super().save(*args, **kwargs)
        else:
            raise ValueError("Only Admin, Manager, or Team Leader can assign tasks.")

    def __str__(self):
        return f"{self.task.task_title} assigned to {self.assigned_to.full_name}"
