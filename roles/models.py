from django.db import models
from django.contrib.auth.models import User, Permission

class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return self.role_name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"
