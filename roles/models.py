from django.db import models
from django.contrib.auth.models import User, Permission
from department.models import Department

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles", null=True, blank=True)  # ✅ Allow NULL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return f"{self.role_name} ({self.department.dept_name if self.department else 'No Department'})"  # ✅ Handle NULL department


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)  # Ensure this exists
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Add department
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name if self.role else 'No Role'}"

