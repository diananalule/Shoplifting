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
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.datastructures import MultiValueDictKeyError
import http.client
import json

# Create your views here.
def home(request):
    if  request.user.is_authenticated:
        return render(request, 'pages/home.html', {'user': request.user})
    return render(request, 'index.html', {'failed':'false'})

def log_out(request):
    request.session.flush()
    return render(request, 'index.html', {'failed':'false'})
    
def add_student(request):
    user = request.user
    return render(request, 'pages/addStudent.html', {'user': user})

def save_student(request):
    try:
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
        students = Student.objects.filter(created_by=request.user).order_by('-date_added')
        return render(request, 'pages/students.html', {'students': students, 'user': request.user})
    except MultiValueDictKeyError:
        return render(request, 'pages/addStudent.html', {'error': 'No image data found in the request', 'user': request.user})

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
    conn = http.client.HTTPSConnection( "8gw2rr.api.infobip.com")
    payload = json.dumps({
        "messages": [
            {
                "destinations": [
                    {
                        "to": "+256758237196"
                    }
                ],
                "from": "InfoSMS",
                "text": "Attention: Suspicious activity detected. Please review your surveillance footage immediately for any unusual behavior or potential security breaches. If anything concerning is found, contact security or law enforcement right away. Ensure to save and back up the footage for further investigation. Your prompt attention is crucial. Stay vigilant and safe."
            }
        ]
    })
    headers = {
        'Authorization': "App 5ca985a8a07f37684be5df1d37440fad-e7b6789e-ca0d-4afa-b832-6ec888bd64c9",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    print("message")
    return JsonResponse({'status':'success', 'message': "sms_response"}, status=200)