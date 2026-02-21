from django import forms
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Staff, Leave, Payslip
from core.models import User

class StaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    role = forms.ChoiceField(choices=[
        (User.Role.TEACHER, 'Teacher'),
        (User.Role.STAFF, 'Staff'),
        (User.Role.TRANSPORT_MANAGER, 'Transport Manager'),
        (User.Role.ADMIN, 'Admin')
    ], initial=User.Role.TEACHER, label='Role')
    photo = forms.ImageField(required=False, label='Photo', help_text='Upload a passport-size photo')

    class Meta:
        model = Staff
        exclude = ('user',)
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-fill User data
            if self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email
                self.fields['role'].initial = self.instance.user.role
            if self.instance.photo:
                self.fields['photo'].initial = self.instance.photo

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ('photo_preview', 'get_full_name', 'designation', 'department', 'employee_id', 'get_role')
    list_filter = ('department', 'designation', 'user__role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return mark_safe('<span style="display:inline-block;width:36px;height:36px;border-radius:50%;background:#E5E7EB;text-align:center;line-height:36px;font-size:14px;color:#6B7280;">👤</span>')
    photo_preview.short_description = 'Photo'

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "-"
    get_full_name.short_description = 'Name'

    def get_role(self, obj):
        return obj.user.get_role_display() if obj.user else "-"
    get_role.short_description = 'Role'

    def save_model(self, request, obj, form, change):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        role = form.cleaned_data.get('role')

        if not change:
            # Create User
            username = f"{first_name.lower()}_{get_random_string(4).lower()}"
            password = get_random_string(12)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            obj.user = user
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            obj.save()
            
            # Send Credentials
            try:
                send_mail(
                    'Your Staff Portal Credentials - SMS',
                    f'Dear {first_name},\n\n'
                    f'Welcome to School Management System!\n\n'
                    f'Your account has been created. Please log in using the credentials below:\n\n'
                    f'Username: {username}\n'
                    f'Password: {password}\n\n'
                    f'Best Regards,\nSchool Administration',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f"Staff created and credentials sent to {email}")
            except Exception as e:
                messages.warning(request, f"Staff created but email failed: {e}")
        else:
            # Update User
            user = obj.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            user.save()
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            super().save_model(request, obj, form, change)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('staff__user__username',)

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'net_salary')
    list_filter = ('month',)
    search_fields = ('staff__user__username',)
