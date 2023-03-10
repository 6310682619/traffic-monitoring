from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from user.models import Account
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('task:index'))
        else:
            return render(request, 'user/signin.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'user/signin.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST.get('confirmpassword')

        # Check if the passwords and username is in correct format
        
        if password != confirmpassword and User.objects.filter(username=username).exists():
            message1 = 'Passwords do not match'
            message2 = 'Username already taken'
            return render(request, 'user/signup.html', {'message1': message1, 'message2': message2})
        
        if password != confirmpassword:
            message1 = 'Passwords do not match'
            return render(request, 'user/signup.html', {'message1': message1})

        if User.objects.filter(username=username).exists():
            message2 = 'Username already taken'
            return render(request, 'user/signup.html', {'message2': message2})

        # Create a new user account
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        )
        account = Account.objects.create(user=user)
        login(request, user)
        return HttpResponseRedirect(reverse('task:index',))
    else:
        return render(request, 'user/signup.html')