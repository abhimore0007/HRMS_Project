from django.urls import path
from . import views  # Import views properly

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/update/<int:task_id>/', views.task_update, name='task_update'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('task/assign/', views.assign_task, name='assign_task'),
    # path('task/update-status/<int:assignment_id>/', views.update_task_status, name='update_task_status'),
]
