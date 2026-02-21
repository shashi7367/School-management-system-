from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('grades/', views.student_grades, name='grades'),
    path('fees/', views.student_fees, name='fees'),
    path('homework/', views.student_homework, name='homework'),
    path('timetable/', views.student_timetable, name='timetable'),
    path('report-card/', views.download_report_card, name='report_card'),
    path('profile/', views.student_profile, name='profile'),
]
