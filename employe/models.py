from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

class Employe_User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(
        "department.Department",  # ✅ Use string reference
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees"
    )
    role = models.ForeignKey(
        "roles.Role",  # ✅ Use string reference
        on_delete=models.SET_NULL,
        null=True,
        related_name="users"
    )
    reporting_manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="team_members"
    )
    date_of_joining = models.DateField(null=True, blank=True,default='2025-01-01')  # ✅ Allows NULL values
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Set email as the unique username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "mobile"]

    def save(self, *args, **kwargs):
        if not self.reporting_manager:
            Role = apps.get_model("roles", "Role")  # ✅ Fetch Role dynamically
            Employe_User = apps.get_model("employe", "Employe_User")  # ✅ Fetch Employe_User dynamically
            
            hr_admin = Employe_User.objects.filter(role__role_name="HR").first()
            self.reporting_manager = hr_admin if hr_admin else None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role.role_name if self.role else 'No Role'}"
