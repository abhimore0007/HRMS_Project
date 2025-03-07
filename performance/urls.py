from django.urls import path
from .views import performance_reviews, add_review, edit_review, delete_review

urlpatterns = [
    path('reviews/', performance_reviews, name='review_list'),
    path('reviews/add/', add_review, name='add_review'),
    path('reviews/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete_review'),
]
