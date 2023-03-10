from celery import shared_task
import sys
sys.path.append('./arial-car-track')
from detect_class import Detect
from opt import Opt
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path

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
        # video = Path('./media/uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/' + file_name)
        # video = './uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/' + file_name
        video = './uploads/' + file_name
        # f = video_path.open(mode='rb')
        # video = File(f)
        result = Result.objects.create(input=input, video=video, weather='')

        report_result = './media/uploads/' + str(user.username) + '/' + str(task.id) + '/object_tracking/loop.txt'
        report_car = []
        f = open(report_result, "r")
        for x in f:
            report_car.append(x.split(','))
        print(report_car)

        car = TotalCar.objects.create(result=result, type="car", total=len(report_car))
        task.status = Task.STATUS_SUCCESS
    except Exception as e:
        print(e)
        task.status = Task.STATUS_ERROR
    task.save()
    return "finish!"