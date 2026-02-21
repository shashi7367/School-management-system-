from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from students.models import Student
from staff.models import Staff
from finance.models import Payment, Invoice
from academics.models import Class, Subject, Exam, Attendance
from transport.models import Vehicle, Route
from .models import User, Announcement
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.is_authenticated and user.role == User.Role.ADMIN

@login_required
def dashboard_router(request):
    if request.user.role == User.Role.ADMIN:
        return redirect('admin_dashboard')
    elif request.user.role == User.Role.STUDENT:
        return redirect('students:dashboard')
    elif request.user.role in [User.Role.TEACHER, User.Role.STAFF]:
        if hasattr(request.user, 'driver_profile'):
             return redirect('transport:driver_dashboard')
        return redirect('staff:dashboard')
    elif request.user.role == User.Role.TRANSPORT_MANAGER:
        return redirect('transport:dashboard')

    return render(request, 'core/access_denied.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Academics
    total_students = Student.objects.count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    
    # Staff
    total_staff = Staff.objects.count()
    
    # Finance
    total_revenue = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    pending_invoices = Invoice.objects.filter(is_paid=False).count()
    
    # Transport
    total_vehicles = Vehicle.objects.count()
    total_routes = Route.objects.count()
    
    # Announcements
    recent_announcements = Announcement.objects.all().order_by('-date_posted')[:5]

    context = {
        'total_students': total_students,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'total_staff': total_staff,
        'total_revenue': total_revenue,
        'pending_invoices': pending_invoices,
        'total_vehicles': total_vehicles,
        'total_routes': total_routes,
        'recent_announcements': recent_announcements,
    }
    return render(request, 'core/admin_dashboard.html', context)

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            email = user.email
            if not email:
                messages.error(request, 'No email address associated with this account. Please contact administrator.')
                return redirect('forgot_password')
                
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['reset_username'] = username
            
            subject = 'Password Reset OTP'
            message = f'Your OTP to reset your password is {otp}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, email_from, recipient_list)
            # Mask email for privacy
            masked_email = email[0:2] + "****" + email[email.find('@'):]
            messages.success(request, f'OTP sent to your registered email ({masked_email}).')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            
    return render(request, 'core/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        try:
            if session_otp and int(otp) == int(session_otp):
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP.')
        except (ValueError, TypeError):
             messages.error(request, 'Invalid OTP format.')
            
    return render(request, 'core/verify_otp.html')

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            username = request.session.get('reset_username')
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                
                # Cleanup session
                if 'otp' in request.session:
                    del request.session['otp']
                if 'reset_username' in request.session:
                    del request.session['reset_username']
                if 'otp_verified' in request.session:
                    del request.session['otp_verified']
                
                messages.success(request, 'Password reset successful. You can now login.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'core/reset_password.html')


@login_required
def profile_router(request):
    """Redirect the user to their role-specific profile page."""
    if request.user.role == User.Role.ADMIN:
        return redirect('admin_profile')
    elif request.user.role == User.Role.STUDENT:
        return redirect('students:profile')
    elif request.user.role in [User.Role.TEACHER, User.Role.STAFF]:
        if hasattr(request.user, 'driver_profile'):
            return redirect('transport:driver_profile')
        return redirect('staff:profile')
    elif request.user.role == User.Role.TRANSPORT_MANAGER:
        return redirect('transport:driver_profile')
    return redirect('dashboard_router')


@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    """Admin profile page with account info and system stats."""
    total_students = Student.objects.count()
    total_staff = Staff.objects.count()
    total_users = User.objects.count()
    total_vehicles = Vehicle.objects.count()

    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'total_users': total_users,
        'total_vehicles': total_vehicles,
    }
    return render(request, 'core/admin_profile.html', context)
