from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='dashboard'),
    path('attendance/select/', views.select_attendance_class, name='select_attendance_class'),
    path('attendance/<int:class_id>/', views.take_attendance, name='take_attendance'),
    path('marks/select/', views.select_exam, name='select_exam'),
    path('marks/<int:exam_id>/', views.enter_marks, name='enter_marks'),
    path('timetable/', views.view_timetable, name='timetable'),
    path('logs/salary/', views.view_salary, name='view_salary'),
    path('homework/assign/', views.assign_homework, name='assign_homework'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('profile/', views.staff_profile, name='profile'),
]
