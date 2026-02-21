from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    current_class = models.ForeignKey('academics.Class', on_delete=models.SET_NULL, null=True, blank=True)
    parents = models.ManyToManyField('students.Parent', related_name='all_children', blank=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.admission_number})"

class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


