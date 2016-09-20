from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register/register_success')
    else:
        form = CustomUserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'userauth/register.html', args)

def register_success(request):
    return render(request, 'userauth/register_success.html')
