import base64
import io
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Student, Image, Attendance
import base64
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.core.files.base import ContentFile
from deepface import DeepFace
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
def home(request):
    return render(request, 'index.html')

def log_out(request):
    request.session.flush()
    
def add_student(request):
    user = request.user
    return render(request, 'pages/addStudent.html', {'user': user})

@login_required
def save_student(request):
    name = request.POST['name']
    student_no = request.POST['student-number']
    course = request.POST['course']
    gender = request.POST['gender']
    images = request.POST['images']
    student = Student.objects.create(name=name, student_no=student_no, course=course, gender=gender)
    if images:
        images = images.split(",")
    for img_data in images:
        img_data = img_data.strip()
        try:
            img_data = base64.b64decode(img_data) 
        except base64.binascii.Error:
            continue 
        img_io = io.BytesIO(img_data)  
        image_name = f"name/{student_no}_image.png"  
        image_file = ContentFile(img_io.getvalue(), name=image_name)  
        uploaded_file = InMemoryUploadedFile(image_file, None, image_name, 'image/png', len(img_data), None)
        image = Image(student=student, image=uploaded_file)
        image.save()
    students = Student.objects.all()
    return redirect('/students')

def capture(request):
    return render(request, 'pages/home.html')
    
def students(request):
    students = Student.objects.all()
    user = request.user
    return render(request, 'pages/students.html', {'students': students, 'user': user})

def attendance(request):
    user = request.user
    return render(request, 'pages/attendance.html', {'students': students, 'user': user})
    

def sign_in_user(request):
    username = request.POST['name']   
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user == None:
        return render(request, 'index.html')
    else:
        return render(request, 'pages/home.html', {'user': user})
    
def verify(request):
    data = json.loads(request.body.decode('utf-8'))
    image_data_uri = data.get('image')
    if image_data_uri:
        _, base64_data = image_data_uri.split(',')
        binary_data = base64.b64decode(base64_data)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(current_directory, 'received_image.jpg')
        with open(save_path, 'wb') as f:
            f.write(binary_data) 
        media_dir = 'media'
        for root, dirs, files in os.walk(media_dir):
            print(dirs)
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                for filename in os.listdir(folder_path):
                    print(filename)
                    if filename.endswith('.jpg') or filename.endswith('.png'):
                        image_path = os.path.join(folder_path, filename)
                        result = DeepFace.verify(image_path, os.path.join(current_directory, 'received_image.jpg'))
                        if result['verified']:
                            print(f"Image {image_path} matches with the saved image.")
                        else:
                            print(f"Image {image_path} does not match with the saved image.")
        return JsonResponse({'message': 'Image saved successfully'})
    else:
        return JsonResponse({'error': 'No image data found in the request'}, status=400)