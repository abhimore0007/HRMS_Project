from django.db import models
from employe.models import Employe_User
# Create your models here.

class LeaveQuota(models.Model):
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=[('SL', 'Sick Leave'), ('CL', 'Casual Leave'), ('PL', 'Paid Leave'), ('LWP', 'Leave Without Pay')])
    total_quota = models.IntegerField()
    used_quota = models.IntegerField(default=0)
    remain_quota = models.IntegerField()

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"

# Leave Request Model
class Leave(models.Model):
    STATUS_CHOICES = [('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')]

    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=[('SL', 'Sick Leave'), ('CL', 'Casual Leave'), ('PL', 'Paid Leave'), ('LWP', 'Leave Without Pay')])
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employe_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"
