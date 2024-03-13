from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

def user_images_path(instance, filename):
    username = instance.student.name if instance.student.name else 'unknown_user'
    return os.path.join('images', username, filename)

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_no = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
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
