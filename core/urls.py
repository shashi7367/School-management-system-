from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_router, name='dashboard_router'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('login/student/', auth_views.LoginView.as_view(template_name='core/login_student.html'), name='login_student'),
    path('login/teacher/', auth_views.LoginView.as_view(template_name='core/login_teacher.html'), name='login_teacher'),
    path('login/driver/', auth_views.LoginView.as_view(template_name='core/login_driver.html'), name='login_driver'),
    path('login/admin/', auth_views.LoginView.as_view(template_name='core/login_admin.html'), name='login_admin'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_router, name='profile_router'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
]
