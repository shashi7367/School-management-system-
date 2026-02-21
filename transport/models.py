from django.conf import settings
from django.db import models
# Use string reference for Student to avoid circular imports if possible, or import inside methods, but here it's foreign key.
# It seems safer to use 'students.Student' string reference.

class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.license_number})"

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    model = models.CharField(max_length=50)
    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_vehicle')

    def __str__(self):
        return f"{self.model} ({self.registration_number})"

class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    stops = models.TextField(help_text="Comma-separated list of stops")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')

    def __str__(self):
        return self.name

class StudentTransport(models.Model):
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='transport_details')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_point = models.CharField(max_length=100)
    drop_point = models.CharField(max_length=100)
    bus_fees = models.DecimalField(max_digits=8, decimal_places=2, help_text="Monthly/Termly Fees")

    def __str__(self):
        return f"Transport for {self.student}"

class TransportAttendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    is_present_pickup = models.BooleanField(default=False)
    is_present_drop = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date', 'route')

    def __str__(self):
        return f"{self.student} - {self.date}"

class MaintenanceLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    serviced_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Maintenance {self.vehicle} - {self.date}"

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    date = models.DateField()
    liters = models.DecimalField(max_digits=5, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    odometer_reading = models.PositiveIntegerField()

    def __str__(self):
        return f"Fuel {self.vehicle} - {self.date}"
