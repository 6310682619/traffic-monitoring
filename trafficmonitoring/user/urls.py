from django.urls import path, re_path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]