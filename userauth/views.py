from django.shortcuts import render
from .forms import CustomUserCreationForm, LogInForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django import forms
from blog.models import Post
from game_calendar.models import Event
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

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
            return HttpResponseRedirect('/')
    else:
        form = LogInForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'userauth/login.html', args)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_success(request):
    return render(request, 'userauth/login_success.html')

def logout_success(request):
    return render(request, 'userauth/logout_success.html')

@login_required
def dashboard_view(request):
    posts = Post.objects.filter(author=request.user)
    events = Event.objects.filter(author=request.user)
    return render(request, 'userauth/dashboard.html', {'posts': posts, 'events': events})

@login_required
def user_edit(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)
    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST)
        if form.is_valid():
            if users:
                raise forms.ValidationError('A user with that email already exists.')
                return render(request, 'userauth/user_edit.html', {'user': user, 'form': form})
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            users = CustomUser.objects.filter(email__iexact=email).exclude(pk=user.pk)
            user.save()
            return render(request, 'userauth/dashboard_view.html', {'user': user})
    return render(request, 'userauth/user_edit.html', {'user': user, 'form': form})
