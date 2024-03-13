from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_no = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name