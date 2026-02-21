from django import forms
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Student, Parent
from core.models import User

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Joining Date')
    photo = forms.ImageField(required=False, label='Photo', help_text='Upload a passport-size photo')

    class Meta:
        model = Student
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If editing an existing student, pre-fill user fields
            if self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email
            if self.instance.photo:
                self.fields['photo'].initial = self.instance.photo

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('photo_preview', 'get_full_name', 'get_email', 'admission_number', 'current_class', 'date_of_birth')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'admission_number')
    list_filter = ('current_class',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return mark_safe('<span style="display:inline-block;width:36px;height:36px;border-radius:50%;background:#E5E7EB;text-align:center;line-height:36px;font-size:14px;color:#6B7280;">👤</span>')
    photo_preview.short_description = 'Photo'
    
    # Custom display methods
    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return "No User"
    get_full_name.short_description = 'Name'
    
    def get_email(self, obj):
        if obj.user:
            return obj.user.email
        return "No User"
    get_email.short_description = 'Email'

    def save_model(self, request, obj, form, change):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        
        if not change:
            # Create new User
            # username based on admission number to be unique and predictable
            username = f"{obj.admission_number.lower()}"
            
            # Generate random password
            password = get_random_string(length=12)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.STUDENT
            )
            obj.user = user
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            obj.save()
            
            # Send Credentials via Email
            try:
                send_mail(
                    'Your Student Portal Credentials - SMS',
                    f'Dear {first_name},\n\n'
                    f'Welcome to School Management System!\n\n'
                    f'Your account has been created. Please log in using the credentials below:\n\n'
                    f'Username: {username}\n'
                    f'Password: {password}\n\n'
                    f'Please change your password after your first login.\n\n'
                    f'Best Regards,\nSchool Administration',
                    settings.EMAIL_HOST_USER, # From Settings
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f"Student created and credentials sent to {email}")
            except Exception as e:
                messages.warning(request, f"Student created but email failed: {e}")
                
        else:
            # Update existing User
            if obj.user:
                user = obj.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            super().save_model(request, obj, form, change)

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
