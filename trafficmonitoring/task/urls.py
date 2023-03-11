from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<int:task_id>', views.counting_result, name='result'),
    path('create_task', views.create_task, name='create_task'),
    path('mytask/', views.my_task, name='mytask'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
