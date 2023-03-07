from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User
from user.models import Account

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))
    
    task = Task.objects.all().order_by('-date_time')

    return render(request, 'task/index.html', {
        'task': task,
    })

def counting_result(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))
    
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    result = Result.objects.get(input=input)
    loop = Loop.objects.filter(input=input)
    totalcar = TotalCar.objects.filter(input=input)

    if request.method == 'POST':
        loop_id = request.POST['loop_id']
        car = Car.objects.filter(loop=Loop.objects.get(id=loop_id))
        return render(request, 'task/result.html', {
            'task': task,
            'result': result,
            'loop': loop,
            'totalcar': totalcar,
            'car': car
        })
    return render(request, 'task/result.html', {
        'task': task,
        'result': result,
        'loop': loop,
        'totalcar': totalcar
    })

def create_task(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        account = Account.objects.get(user=user)
        name = request.POST['name']
        location = request.POST['location']
        description = request.POST['description']   

        task = Task.objects.create(account=account, name=name,
                                   location=location, description=description)
        
        video = request.FILES['video']
        Input.objects.create(task=task, video=video)

        return HttpResponseRedirect(reverse('task:mytask'))
    
    return render(request, 'task/create_task.html')

def my_task(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))
    
    user = User.objects.get(username=request.user.username)
    account = Account.objects.get(user=user)
    task = Task.objects.filter(account=account).order_by('-date_time')

    return render(request, 'task/mytask.html', {
        'task': task,
    })
