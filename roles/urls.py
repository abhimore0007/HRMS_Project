from django.urls import path
from . import views  # Import the views module

urlpatterns = [
    path('', views.role_list, name='role_list'),
    path('create/<int:dept_id>/', views.create_role, name='create_role'),
    path('update/<int:role_id>/', views.update_role, name='update_role'),
    path('delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('assign/', views.assign_role, name='assign_role'),
    # path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('roles/activate/<int:role_id>/', views.activate_role, name='activate_role'),
]
