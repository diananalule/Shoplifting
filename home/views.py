from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

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
    student_no = request.POST['student_no']
    course = request.POST['course']
    gender = request.POST['gender']
    images = request.FILES['images']
    print(name, student_no, course, gender, images)
    return render(request, 'pages/students.html', {'user': request.user})
    

def sign_in_user(request):
    username = request.POST['name']   
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user == None:
        return render(request, 'index.html')
    else:
        return render(request, 'pages/home.html', {'user': user})