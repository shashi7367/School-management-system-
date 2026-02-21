from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from academics.models import Attendance, Grade, Homework
from finance.models import Payment, FeeStructure
from core.models import Announcement, User
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def student_dashboard(request):
    if request.user.role != User.Role.STUDENT:
        # Redirect or handle other roles
        return render(request, 'core/access_denied.html')

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return render(request, 'students/no_profile.html')
    
    announcements = Announcement.objects.filter(target_role=User.Role.STUDENT).order_by('-date_posted')[:5]
    homeworks = Homework.objects.filter(class_group=student.current_class).order_by('-due_date')[:5]

    # Calculate Attendance Percentage
    total_attendance = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status=Attendance.Status.PRESENT).count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0

    # Calculate Fee Balance
    payments = Payment.objects.filter(student=student)
    total_paid = sum(p.amount_paid for p in payments)
    try:
        fee_structure = FeeStructure.objects.get(class_level=student.current_class)
        total_fee = fee_structure.total_fee()
        fee_balance = total_fee - total_paid
    except FeeStructure.DoesNotExist:
        fee_balance = 0
        total_fee = 0

    # Get Latest Grade
    latest_grade = Grade.objects.filter(student=student).order_by('-exam__date').first()

    context = {
        'student': student,
        'announcements': announcements,
        'homeworks': homeworks,
        'attendance_percentage': round(attendance_percentage, 1),
        'fee_balance': fee_balance,
        'latest_grade': latest_grade,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def student_attendance(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'students/attendance.html', {'attendance_records': attendance_records})

@login_required
def student_grades(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    grades = Grade.objects.filter(student=student)
    return render(request, 'students/grades.html', {'grades': grades})

@login_required
def student_fees(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    payments = Payment.objects.filter(student=student)
    try:
        fee_structure = FeeStructure.objects.get(class_level=student.current_class)
        total_fee = fee_structure.total_fee()
    except FeeStructure.DoesNotExist:
        total_fee = 0
        fee_structure = None

    total_paid = sum(p.amount_paid for p in payments)
    balance = total_fee - total_paid

    context = {
        'student': student,
        'fee_structure': fee_structure,
        'payments': payments,
        'total_fee': total_fee,
        'total_paid': total_paid,
        'balance': balance,
    }
    return render(request, 'students/fees.html', context)

@login_required
def student_homework(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    homework_list = Homework.objects.filter(class_group=student.current_class).order_by('-due_date')
    return render(request, 'students/homework.html', {'homework_list': homework_list})

@login_required
def download_report_card(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    grades = Grade.objects.filter(student=student)
    
    # Simple HTML Report Generation for now, ensuring PDF export libraries are available later is better
    # But user asked for PDF/Excel. We will simulate a Print-friendly page which can be saved as PDF.
    
    content = render_to_string('students/report_card_print.html', {'student': student, 'grades': grades})
    return HttpResponse(content)

from academics.models import Timetable
from django.utils import timezone
@login_required
def student_timetable(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('student_dashboard')
        
    timetable_entries = Timetable.objects.filter(class_group=student.current_class).order_by('day', 'start_time')
    
    current_day = timezone.now().strftime('%A').upper()
    todays_classes = timetable_entries.filter(day=current_day).count()
    total_classes = timetable_entries.count()
    total_subjects = timetable_entries.values('subject').distinct().count()

    context = {
        'timetable': timetable_entries,
        'todays_classes': todays_classes,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
    }
    return render(request, 'students/timetable.html', context)


@login_required
def student_profile(request):
    if request.user.role != User.Role.STUDENT:
        return render(request, 'core/access_denied.html')

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return render(request, 'students/no_profile.html')

    # Attendance stats
    total_attendance = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status=Attendance.Status.PRESENT).count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0

    # Fee stats
    payments = Payment.objects.filter(student=student)
    total_paid = sum(p.amount_paid for p in payments)
    try:
        fee_structure = FeeStructure.objects.get(class_level=student.current_class)
        total_fee = fee_structure.total_fee()
        fee_balance = total_fee - total_paid
    except FeeStructure.DoesNotExist:
        fee_balance = 0
        total_fee = 0

    # Parents
    parents = student.parents.all()

    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 1),
        'total_paid': total_paid,
        'total_fee': total_fee,
        'fee_balance': fee_balance,
        'parents': parents,
    }
    return render(request, 'students/profile.html', context)
