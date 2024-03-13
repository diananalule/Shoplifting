from django.urls import path
from .views import home, sign_in_user, log_out, add_student

urlpatterns = [
    path('', home, name='home'),
    path('sign_in', sign_in_user, name='sign_in'),
    path('logout', log_out, name='logout'),
    path('add_student', add_student, name='add_student')
]