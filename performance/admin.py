from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'review_title', 'employee', 'reviewed_by', 'review_period', 'rating', 'review_date')
    search_fields = ('review_title', 'employee__first_name', 'reviewed_by__first_name')
    list_filter = ('review_period', 'rating')
