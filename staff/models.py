from django.conf import settings
from django.db import models

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    designation = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.designation})"

class Leave(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')

    def __str__(self):
        return f"{self.staff} - {self.start_date} to {self.end_date}"

class Payslip(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='payslips')
    month = models.DateField(help_text="First day of the month")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.allowances - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payslip for {self.staff} - {self.month.strftime('%B %Y')}"
