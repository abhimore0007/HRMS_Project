from django.db import models
from django.contrib.auth.models import AbstractUser
from department.models import Department
from roles.models import Role

class User(AbstractUser):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name="users")
    reporting_manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override username field to remove restrictions
    username = models.CharField(max_length=150, unique=True, blank=False)

    # Fix conflicts with Django's auth.User model
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.reporting_manager:
            hr_admin = User.objects.filter(role__role_name="HR").first()
            self.reporting_manager = hr_admin if hr_admin else None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role.role_name if self.role else 'No Role'}"
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="department_employees")  # ✅ Unique related_name
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    reporting_manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role.role_name if self.role else 'No Role'}"


