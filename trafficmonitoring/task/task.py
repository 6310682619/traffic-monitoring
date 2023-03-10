from celery import shared_task
import sys
sys.path.append('./arial-car-track')
from detect_class import Detect
from opt import Opt
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User


@shared_task()
def detect_track(opt_json, task_id):
    task = Task.objects.get(id=task_id)
    try:
        opt = Opt()
        opt.set_opt(opt_json)
        detect = Detect(opt)
        detect.run()

        input = Input.objects.get(task=task)
        user = User.objects.get(username=task.account.user.username) 
        file_name = str(input.video).split('/')[1]

        video = './uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/' + file_name

        result = Result.objects.create(input=input, video=video)

        report_result = './media/uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/loop.txt'
        report_car = []
        try:
            f = open(report_result, "r")
            for x in f:
                report_car.append(x.split(','))
            print(report_car)
        except:
            pass
        
        temp = []
        for i in range(len(report_car)):
            type_car = report_car[i][2]
            if(type_car in temp):
                totalcar = TotalCar.objects.get(result=result, type=type_car)
                totalcar.total += 1
                totalcar.save()
            else:
                totalcar = TotalCar.objects.create(result=result, type=type_car, total=1)
                temp.append(type_car)
            
        task.status = Task.STATUS_SUCCESS
    except Exception as e:
        print(e)
        task.status = Task.STATUS_ERROR
    task.save()
    return "finish!"