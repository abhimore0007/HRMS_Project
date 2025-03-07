from django.db import models
from employe.models import Employe_User  # Import the Employee model

class PerformanceReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_title = models.CharField(max_length=100)
    review_date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE, related_name="reviews_received")
    reviewed_by = models.ForeignKey(Employe_User, on_delete=models.CASCADE, related_name="reviews_given")
    review_period = models.CharField(
        max_length=100, 
        choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annual', 'Annual')]
    )
    rating = models.IntegerField()
    comments = models.TextField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.review_title} - {self.employee.first_name} {self.employee.last_name}"
