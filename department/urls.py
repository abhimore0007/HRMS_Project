from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('Department', views.department_dashboard, name='department_dashboard'),
    path('departments/<int:dept_id>/', views.department_details, name='department_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path('add/', views.add_department, name='add_department'),
    path('update/<int:dept_id>/', views.update_department, name='update_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('no_role/', views.no_role, name='no_role_page'),
    path('Forgot_Password/', views.Forgot_pass, name='Forgotpass'),  # Add this new view
    path('success/', views.success_page, name='success_page'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),

]

