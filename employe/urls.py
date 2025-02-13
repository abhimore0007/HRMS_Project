from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.create_employee, name='create_employee'),
    path('list/', views.employee_list, name='employee_list'),
    path('employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]
