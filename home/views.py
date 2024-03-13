from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def home(request):
    return render(request, 'index.html')

def log_out(request):
    request.session.flush()
    
def add_student(request):
    return render(request, 'pages/addStudent.html')

def sign_in_user(request):
    username = request.POST['name']   
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user == None:
        return render(request, 'index.html')
    else:
        return render(request, 'pages/home.html', {'user': user})