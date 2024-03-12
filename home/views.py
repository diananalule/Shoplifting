from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def home(request):
    return render(request, 'index.html')

def sign_in_user(request):
    email = request.POST['email']   
    password = request.POST['password']
    print(email, password)
    user = authenticate(request, email=email, password=password)
    print(user)
    if user == None:
        return render(request, 'index.html')
    else:
        return render(request, 'pages/home.html')