from django.db import models
from django.contrib.auth.models import Permission
from django.conf import settings
from django.apps import apps  # ✅ Use apps.get_model to prevent circular imports

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    department = models.ForeignKey(
        "department.Department",  # ✅ Use string reference to prevent import issues
        on_delete=models.CASCADE,
        related_name="roles",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return f"{self.role_name} ({self.department.dept_name if self.department else 'No Department'})"


class UserRole(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use dynamic reference
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        "roles.Role",  # ✅ Use string reference to prevent circular imports
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        "department.Department",  # ✅ Use string reference
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.role.role_name if self.role else 'No Role'}"
