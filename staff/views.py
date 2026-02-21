from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Staff, Leave, Payslip
from academics.models import Class, Attendance, Subject, Timetable, Grade, Exam
from students.models import Student
from core.models import User, Announcement

@login_required
def staff_dashboard(request):
    if request.user.role not in [User.Role.TEACHER, User.Role.STAFF]:
         return render(request, 'core/access_denied.html')

    try:
        staff_profile = request.user.staff_profile
    except Staff.DoesNotExist:
         return render(request, 'staff/no_profile.html')

    classes_taught = Class.objects.filter(teacher=staff_profile)
    subjects_taught = Subject.objects.filter(teacher=staff_profile)
    recent_leaves = Leave.objects.filter(staff=staff_profile).order_by('-start_date')[:5]
    announcements = Announcement.objects.filter(target_role__in=[User.Role.TEACHER, User.Role.STAFF]).order_by('-date_posted')[:5]

    context = {
        'staff': staff_profile,
        'classes': classes_taught,
        'subjects': subjects_taught,
        'recent_leaves': recent_leaves,
        'announcements': announcements,
    }
    return render(request, 'staff/dashboard.html', context)

@login_required
def select_attendance_class(request):
    # Fetch all classes so any teacher can take attendance (e.g. substitute)
    # You might want to filter this based on permissions in a stricter system
    classes = Class.objects.all().order_by('name', 'section')
    return render(request, 'staff/select_attendance_class.html', {'classes': classes})

@login_required
def take_attendance(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(current_class=class_obj)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            Attendance.objects.create(
                student=student, 
                date=date, 
                status=status,
                remarks=remarks
            )
        messages.success(request, f"Attendance marked for {class_obj}")
        return redirect('staff:dashboard')
    
    return render(request, 'staff/take_attendance.html', {'class': class_obj, 'students': students})

@login_required
def select_exam(request):
    exams = Exam.objects.all().order_by('-date')
    return render(request, 'staff/select_exam.html', {'exams': exams})

@login_required
def enter_marks(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(current_class=exam.class_group)

    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            if marks:
                Grade.objects.update_or_create(
                    student=student,
                    exam=exam,
                    defaults={'marks_obtained': marks, 'remarks': remarks}
                )
            else:
                # If marks are cleared, remove the grade entry? 
                # Or just skip. Let's skip for now to avoid accidental deletion, 
                # but in full system might want to allow clearing.
                pass
                
        messages.success(request, f"Marks updated for {exam}")
        return redirect('staff:dashboard')

    # Pre-fetch existing grades to display
    existing_grades = Grade.objects.filter(exam=exam, student__in=students)
    grade_map = {grade.student.id: grade for grade in existing_grades}
    
    # Attach grade to student object temporarily for template
    for student in students:
        student.current_grade = grade_map.get(student.id)

    return render(request, 'staff/enter_marks.html', {'exam': exam, 'students': students})

@login_required
def view_timetable(request):
    staff_profile = request.user.staff_profile
    timetable = Timetable.objects.filter(teacher=staff_profile).order_by('day', 'start_time')
    return render(request, 'staff/timetable.html', {'timetable': timetable})

@login_required
def apply_leave(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        Leave.objects.create(
            staff=request.user.staff_profile,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        messages.success(request, "Leave application submitted.")
        return redirect('staff:dashboard')
    return render(request, 'staff/apply_leave.html')

@login_required
def view_salary(request):
    payslips = Payslip.objects.filter(staff=request.user.staff_profile).order_by('-month')
    return render(request, 'staff/view_salary.html', {'payslips': payslips})

from academics.models import Homework
@login_required
def assign_homework(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        class_group = get_object_or_404(Class, id=class_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        Homework.objects.create(
            class_group=class_group,
            subject=subject,
            title=title,
            description=description,
            assigned_date=request.POST.get('assigned_date'), # Assuming we send today or user picked
            due_date=due_date,
            assigned_by=request.user.staff_profile
        )
        messages.success(request, "Homework assigned successfully.")
        return redirect('staff:dashboard')

    # Data for the form
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    from django.utils import timezone
    today = timezone.now().date()
    
    return render(request, 'staff/assign_homework.html', {
        'classes': classes, 
        'subjects': subjects,
        'today': today
    })


@login_required
def staff_profile(request):
    if request.user.role not in [User.Role.TEACHER, User.Role.STAFF]:
        return render(request, 'core/access_denied.html')

    try:
        staff_profile = request.user.staff_profile
    except Staff.DoesNotExist:
        return render(request, 'staff/no_profile.html')

    classes_taught = Class.objects.filter(teacher=staff_profile)
    subjects_taught = Subject.objects.filter(teacher=staff_profile)
    recent_leaves = Leave.objects.filter(staff=staff_profile).order_by('-start_date')[:5]
    payslips = Payslip.objects.filter(staff=staff_profile).order_by('-month')[:3]

    context = {
        'staff': staff_profile,
        'classes': classes_taught,
        'subjects': subjects_taught,
        'recent_leaves': recent_leaves,
        'payslips': payslips,
    }
    return render(request, 'staff/profile.html', context)
