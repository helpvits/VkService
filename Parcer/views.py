from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
# Create your views here.
from django.template.context_processors import csrf


def home(request):
    return render_to_response('base.html')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)


# df