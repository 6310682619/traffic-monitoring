from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'user/signin.html')

def signup(request):
    return render(request, 'user/signup.html')