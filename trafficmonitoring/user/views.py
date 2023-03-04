from django.shortcuts import render, redirect

# Create your views here.

def signin(request):
    return render(request, 'user/signin.html')

def signup(request):
    return render(request, 'user/signup.html')