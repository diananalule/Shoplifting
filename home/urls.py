from django.urls import path
from .views import home, sign_in_user

urlpatterns = [
    path('', home, name='home'),
    path('sign_in', sign_in_user, name='sign_in')
]