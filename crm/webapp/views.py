from django.shortcuts import render, redirect

from django.http import HttpResponse
from .forms import CreateUserForms, LoginForm

from django import forms
from django.forms.widgets import PasswordInput, TextInput

from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# home page


def home(request):
    # return HttpResponse("Hello World")
    return render(request, 'webapp/index.html')

# register


def register(request):
    form = CreateUserForms()
    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            form.save()

            return redirect('my-login')
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)


# Login

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse('Invalid credentials')
    context = {'form': form}
    return render(request, 'webapp/my-login.html', context=context)


# User Logout
def user_logout(request):
    auth.logout(request)
    return redirect('my-login')


# dashboard
@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'webapp/dashboard.html')
