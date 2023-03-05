from django.db import models
from user.models import Account
# Create your models here.
    
class Task(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_time = models.DateTimeField('date_time', auto_now_add=True)
    date_time_modify = models.CharField(max_length=100)
    date_time_upload = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    status = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.date_time}"
    
class Input(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    video = models.FileField(upload_to = 'uploads/', blank=True)

    def __str__(self):
        return f"{self.video}"
    
class Result(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    video = models.FileField(upload_to = 'uploads/', blank=True)
    weather = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.weather}"

class Loop(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    loop_name = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    wigth = models.IntegerField()
    height = models.IntegerField()
    angle = models.IntegerField()

    def __str__(self):
        return f"{self.loop_name}"
class Car(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE)
    car_total = models.IntegerField(default=0)
    car_type = models.CharField(max_length=20)
    direction = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.car_total}"

class TotalCar(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.type}"
