from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

def user_images_path(instance, filename):
    # username = instance.student.name if instance.student.name else 'unknown_user'
    student_number = instance.student.student_no if instance.student.student_no else 'unknown_user'
    return os.path.join('images', student_number, filename)

class Student(models.Model):
    student_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_images_path)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.student.name} ({self.date_added})"
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField(default=timezone.now)
    time_out = models.TimeField(default=timezone.now)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.time_in} - {self.time_out}"
