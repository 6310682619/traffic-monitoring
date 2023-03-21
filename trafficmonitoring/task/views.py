from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Task, Input, Result, Loop, Car, TotalCar
from django.contrib.auth.models import User
from user.models import Account
from .task import detect_track
from opt import OptJson
import cv2
import os
import matplotlib.pyplot as plt
import math

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    task = Task.objects.all().order_by('-date_time')

    return render(request, 'task/index.html', {
        'task': task,
    })

def counting_result(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
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
        return HttpResponseRedirect(reverse('user:signin'))
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        account = Account.objects.get(user=user)
        name = request.POST['name']
        location = request.POST['location']
        description = request.POST['description']   

        task = Task.objects.create(account=account, name=name, location=location,
                                    description=description, status=Task.STATUS_PENDING )
        
        video = request.FILES['video']
        input = Input.objects.create(task=task, video=video)
        cam = cv2.VideoCapture(input.video.path)
        ret, frame = cam.read()
        if ret:
            name = str(input.video.name.split('.')[0]) + ".png"
            cv2.imwrite("./media/frame/" + name, frame)
            input.sample_img = "./frame/" + name
            pic = plt.imread("./media/frame/" + name)
            fig = plt.figure()
            ax = fig.subplots()
            ax.imshow(pic)
            plt.savefig("./media/fig/" + name)
            input.fig_img = "./fig/" + name
            input.save()

        return HttpResponseRedirect(reverse('task:edit_loop', args=(task.id,)))
    
    return render(request, 'task/create_task.html')

def color_line(pt, pt0, pt1, direction):
    if find_line_entry(pt, pt0, pt1, direction):
        color = (255, 0, 30)
    else:
        color = (0, 255, 0)
    return color

def find_line_entry(pt, p0, p1, direction):
    p0 = p0[1], p0[0]
    p1 = p1[1], p1[0]

    max_x, min_x = max([x[0] for x in pt]), min([x[0] for x in pt])
    max_y, min_y = max([x[1] for x in pt]), min([x[1] for x in pt])
        
    if direction == 1:
        return ((max_x == p0[0]) or (max_x == p1[0])) and ((max_y == p0[1]) or (max_y == p1[1]))
    elif direction == 2:
        return ((max_x == p0[0]) and (max_x == p1[0]))
    elif direction == 3:
        return ((max_x == p0[0]) or (max_x == p1[0])) and ((min_y == p0[1]) or (min_y == p1[1]))
    elif direction == 4:
        return ((min_y == p0[1]) and (min_y == p1[1]))
    elif direction == 5:
        return ((min_x == p0[0]) or (min_x == p1[0])) and ((min_y == p0[1]) or (min_y == p1[1]))
    elif direction == 6:
        return ((min_x == p0[0]) and (min_x == p1[0]))
    elif direction == 7:
        return ((min_x == p0[0]) or (min_x == p1[0])) and ((max_y == p0[1]) or (max_y == p1[1]))
    elif direction == 8:
        return ((max_y == p0[1]) and (max_y == p1[1]))



def find_rec(x, y, width, height, angle):
    _angle = -angle * math.pi / 180.0
    b = math.cos(_angle) * 0.5
    a = math.sin(_angle) * 0.5
    pt0 = (int(y - a * height - b * width),
        int(x + b * height - a * width))
    pt1 = (int(y + a * height - b * width),
        int(x - b * height - a * width))
    pt2 = (int(2 * y - pt0[0]), int(2 * x - pt0[1]))
    pt3 = (int(2 * y - pt1[0]), int(2 * x - pt1[1]))

    pt = [pt0, pt1, pt2, pt3]
    for i in range(len(pt)):
        pt[i] = (pt[i][1], pt[i][0])
    
    return pt, pt0, pt1, pt2, pt3

def draw_angled_rec(img, x, y, width, height, angle, thickness, direction):
    pt, pt0, pt1, pt2, pt3 = find_rec(x, y, width, height, angle)
    cv2.line(img, pt0, pt1, color_line(pt, pt0, pt1, direction), thickness)
    cv2.line(img, pt1, pt2, color_line(pt, pt1, pt2, direction), thickness)
    cv2.line(img, pt2, pt3, color_line(pt, pt2, pt3, direction), thickness)
    cv2.line(img, pt3, pt0, color_line(pt, pt3, pt0, direction), thickness)
    return img

def draw_all_loop(input):
    image = cv2.imread(input.sample_img.path)
    name = str(input.video.name.split('.')[0]) + ".png"
    color = (0, 255, 0)
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    for loop in Loop.objects.filter(input=input):
        image = draw_angled_rec(image, loop.x, loop.y, loop.width,
                                loop.height, loop.angle, thickness,
                                loop.direction)
        org = (loop.y, loop.x)
        image = cv2.putText(image, loop.loop_name, org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    fig = plt.figure()
    ax = fig.subplots()
    ax.imshow(image)
    plt.savefig("./media/fig/" + name)
    input.fig_img = "./fig/" + name
    input.save()
    
    
def edit_loop(request, task_id):
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    if request.method == "POST":
        loop_name = request.POST["loop_name"]
        x = int(request.POST["x"])
        y = int(request.POST["y"])
        width = int(request.POST["width"])
        height = int(request.POST["height"])
        angle = int(request.POST["angle"])
        direction = int(request.POST["direction"])

        loop = Loop.objects.create(input=input, loop_name=loop_name, x=x, y=y,
                                   width=width, height=height, angle=angle, direction=direction)
        draw_all_loop(input)
    all_loop = Loop.objects.filter(input=input)
    return render(request, 'task/edit_loop.html', {
        "task": task,
        "input": input,
        "all_loop": all_loop,
    })

def delete_loop(request, loop_id):
    try:
        loop = Loop.objects.get(id=loop_id)
    except:
        return HttpResponseRedirect(reverse('task:index'))
    
    input = loop.input

    loop.delete()
    draw_all_loop(input)
    return HttpResponseRedirect(reverse('task:edit_loop', args=(input.task.id,)))

def add_point(ptx, begin):
    point = []
    for i in range(len(ptx)):
        point.append({"x": ptx[(begin+i)%len(ptx)][0], "y": ptx[(begin+i)%len(ptx)][1]})
    return point

def create_loop(all_loop):
    loops = []
    loops_id = []
    for loop in all_loop:
        points = []
        pt, pt0, pt1, pt2, pt3 = find_rec(loop.x, loop.y, loop.width, loop.height, loop.angle)
        ptx = [pt0, pt1, pt2, pt3]
        if find_line_entry(pt, pt0, pt1, loop.direction):
            points = add_point(ptx, 0)
        elif find_line_entry(pt, pt1, pt2, loop.direction):
            points = add_point(ptx, 1)
        elif find_line_entry(pt, pt2, pt3, loop.direction):
            points = add_point(ptx, 2)
        elif find_line_entry(pt, pt3, pt0, loop.direction):
            points = add_point(ptx, 3)

        loops.append({
            "name": loop.loop_name,
            "id": loop.id,
            "points": points,
            "orientation":"clockwise",
            "summary_location":{"x":0,"y":"0"}
        })
        loops_id.append(loop.id)
    loop_json = {"loops": loops, "loop_id":loops_id}
    return loop_json

def run_task(request, task_id):
    task = Task.objects.get(id=task_id)
    input = Input.objects.get(task=task)
    opt = OptJson
    opt['source'] = input.video.path
    opt['project'] = './media/uploads/' + str(request.user.username) + '/' + str(task.id)
    opt['loop'] = create_loop(Loop.objects.filter(input=input))

    task.status=Task.STATUS_PENDING
    task.save()

    detect_track.delay(opt, task.id)
    return HttpResponseRedirect(reverse('task:mytask'))


def my_task(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(username=request.user.username)
    account = Account.objects.get(user=user)
    task = Task.objects.filter(account=account).order_by('-date_time')

    return render(request, 'task/mytask.html', {
        'task': task,
    })
