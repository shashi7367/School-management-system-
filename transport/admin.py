from django import forms
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Driver, Vehicle, Route, StudentTransport, TransportAttendance, MaintenanceLog, FuelLog
from core.models import User

class DriverForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    
    # Vehicle Details
    vehicle_model = forms.CharField(max_length=50, required=False, label='Bus Name/Model', help_text="e.g. Tata Starbus 2024")
    vehicle_plate = forms.CharField(max_length=20, required=False, label='Number Plate', help_text="e.g. DL-01-AB-1234")
    vehicle_capacity = forms.IntegerField(required=False, label='Bus Capacity', help_text="Seating Capacity", initial=30)
    photo = forms.ImageField(required=False, label='Photo', help_text='Upload a passport-size photo')

    class Meta:
        model = Driver
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-fill User data
            if self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email
            if self.instance.photo:
                self.fields['photo'].initial = self.instance.photo
            
            # Pre-fill Vehicle data (reverse relationship)
            try:
                vehicle = self.instance.assigned_vehicle
                self.fields['vehicle_model'].initial = vehicle.model
                self.fields['vehicle_plate'].initial = vehicle.registration_number
                self.fields['vehicle_capacity'].initial = vehicle.capacity
            except Vehicle.DoesNotExist:
                pass

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    form = DriverForm
    list_display = ('photo_preview', 'get_full_name', 'phone_number', 'license_number', 'get_vehicle')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'phone_number')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return mark_safe('<span style="display:inline-block;width:36px;height:36px;border-radius:50%;background:#E5E7EB;text-align:center;line-height:36px;font-size:14px;color:#6B7280;">👤</span>')
    photo_preview.short_description = 'Photo'

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "No User"
    get_full_name.short_description = 'Name'

    def get_vehicle(self, obj):
        try:
            return obj.assigned_vehicle
        except Vehicle.DoesNotExist:
            return "-"
    get_vehicle.short_description = 'Assigned Bus'

    def save_model(self, request, obj, form, change):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        
        # Vehicle Data
        v_model = form.cleaned_data.get('vehicle_model')
        v_plate = form.cleaned_data.get('vehicle_plate')
        v_cap = form.cleaned_data.get('vehicle_capacity') or 30

        if not change:
            # Create User
            username = f"driver_{get_random_string(6).lower()}"
            password = get_random_string(12)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.STAFF # Drivers are staff
            )
            obj.user = user
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            obj.save()
            
            # Send Credentials
            try:
                send_mail(
                    'Your Driver Portal Credentials - SMS',
                    f'Dear {first_name},\n\n'
                    f'Welcome to School Management System!\n\n'
                    f'Your account has been created. Please log in using the credentials below:\n\n'
                    f'Username: {username}\n'
                    f'Password: {password}\n\n'
                    f'Best Regards,\nSchool Transport Dept',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f"Driver created and credentials sent to {email}")
            except Exception as e:
                messages.warning(request, f"Driver created but email failed: {e}")
        else:
            # Update User
            user = obj.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            if form.cleaned_data.get('photo'):
                obj.photo = form.cleaned_data['photo']
            super().save_model(request, obj, form, change)

        # Handle Vehicle Creation/Update
        if v_model and v_plate:
            # Check if vehicle exists for this driver
            try:
                vehicle = obj.assigned_vehicle
                vehicle.model = v_model
                vehicle.registration_number = v_plate
                vehicle.capacity = v_cap
                vehicle.save()
            except Vehicle.DoesNotExist:
                # Create new vehicle and assign to this driver
                Vehicle.objects.create(
                    registration_number=v_plate,
                    model=v_model,
                    capacity=v_cap,
                    driver=obj
                )

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'model', 'capacity', 'driver')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_point', 'end_point', 'vehicle')
    list_filter = ('vehicle',)

@admin.register(StudentTransport)
class StudentTransportAdmin(admin.ModelAdmin):
    list_display = ('student', 'route', 'pickup_point', 'drop_point', 'bus_fees')
    list_filter = ('route',)
    search_fields = ('student__user__username',)

@admin.register(TransportAttendance)
class TransportAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'route', 'date', 'is_present_pickup', 'is_present_drop')
    list_filter = ('date', 'route')

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'cost', 'serviced_by')
    list_filter = ('vehicle', 'date')

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'liters', 'cost', 'odometer_reading')
    list_filter = ('vehicle', 'date')
