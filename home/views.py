import base64
import io
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student, Image, Attendance
from django.core.exceptions import ObjectDoesNotExist
import base64
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.core.files.base import ContentFile
from deepface import DeepFace
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
def home(request):
    if request.user is not None:
        return render(request, 'pages/home.html', {'user': request.user})
    return render(request, 'index.html', {'failed':'false'})

def log_out(request):
    request.session.flush()
    return render(request, 'index.html', {'failed':'false'})
    
def add_student(request):
    user = request.user
    return render(request, 'pages/addStudent.html', {'user': user})

def save_student(request):
    name = request.POST['name']
    student_no = request.POST['student-number']
    course = request.POST['course']
    gender = request.POST['gender']
    images = request.POST['images']
    student = Student.objects.create(name=name, student_no=student_no, course=course, gender=gender, created_by=request.user)
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
    students = Student.objects.filter(created_by=request.user).order_by('-date_added')
    user = request.user
    return render(request, 'pages/students.html', {'students': students, 'user': user})

def attendance(request):
    user = request.user
    attendances = Attendance.objects.filter(recorded_by=request.user).order_by('-date')
    return render(request, 'pages/attendance.html', {'attendances': attendances, 'user': user})
    

def sign_in_user(request):
    username = request.POST['name']   
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'pages/home.html', {'user': user})
    else:
        return render(request, 'index.html', {'failed':'true'})
    
def verify(request):
    is_in_process = True
    if is_in_process:
        is_in_process = False
        models = [
        "VGG-Face", 
        "Facenet", 
        "Facenet512", 
        "OpenFace", 
        "DeepFace", 
        "DeepID", 
        "ArcFace", 
        "Dlib", 
        "SFace",
        "GhostFaceNet",
        ]
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
                for dir_name in dirs:
                    folder_path = os.path.join(root, dir_name)
                    for filename in os.listdir(folder_path):
                        if filename.endswith('.jpg') or filename.endswith('.png'):
                            image_path = os.path.join(folder_path, filename)
                            result = DeepFace.verify(img1_path = image_path,  img2_path = os.path.join(current_directory, 'received_image.jpg'), model_name = models[1], enforce_detection=False)
                            if result['verified']:
                                try:
                                    if Attendance.objects.filter(date=datetime.now().date()).filter(student=Student.objects.get(student_no=dir_name)).exists():
                                        return JsonResponse({'status':'failed', 'message': 'Student has already been verified'})
                                except ObjectDoesNotExist:
                                    pass
                                Attendance.objects.create(student=Student.objects.get(student_no=dir_name), recorded_by=request.user, date=datetime.now().date(), time_in=datetime.now().time())
                                is_in_process = True
                                return JsonResponse({'status':'success', 'message': 'Image Detected successfully', 'student':str(Student.objects.filter(student_no=dir_name).first())})
                            else:
                                print(f"Image {image_path} does not match with the saved image.")
            return JsonResponse({'status':'failed', 'message': 'Image Detected successfully'})
            is_in_process = True
        else:
            return JsonResponse({'status':'errror', 'error': 'No image data found in the request'}, status=400)