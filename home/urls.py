from django.urls import path
from .views import home, sign_in_user, log_out, add_student, save_student, students, capture, attendance, verify

urlpatterns = [
    path('', home, name='home'),
    path('sign_in', sign_in_user, name='sign_in'),
    path('logout', log_out, name='logout'),
    path('add_student', add_student, name='add_student'),
    path('students', students, name='students'),
    path('save_student', save_student, name='save_student'),
    path('home', capture, name='home'),
    path('attendance', attendance, name='attendance'),
    path('verify', verify, name='verify')
]