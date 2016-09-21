from django.shortcuts import render
from .forms import CustomUserCreationForm, LogInForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django import forms

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/register_success')
    else:
        form = CustomUserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'userauth/register.html', args)

def register_success(request):
    return render(request, 'userauth/register_success.html')

def login_view(request):
    if request.method == 'POST':
        form = LogInForm(data=request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/user/login_success')
    else:
        form = LogInForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'userauth/login.html', args)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/user/logout_success')

def login_success(request):
    return render(request, 'userauth/login_success.html')

def logout_success(request):
    return render(request, 'userauth/logout_success.html')
