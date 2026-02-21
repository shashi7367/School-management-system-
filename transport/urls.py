from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('dashboard/', views.transport_dashboard, name='dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('attendance/<int:route_id>/', views.manage_attendance, name='attendance'),
    path('logs/fuel/', views.log_fuel, name='log_fuel'),
    path('logs/maintenance/', views.log_maintenance, name='log_maintenance'),
    path('driver-profile/', views.driver_profile, name='driver_profile'),
]
