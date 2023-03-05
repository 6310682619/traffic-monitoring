from django.urls import path, re_path
from . import views

app_name = 'task'

urlpatterns = [
    path('result/<int:task_id>', views.counting_result, name='result'),

]