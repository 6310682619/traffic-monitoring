from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Task, Input, Result, Loop, Car, TotalCar
# Create your views here.

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


