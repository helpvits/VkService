from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from Parcer.forms import GroupForm
from Parcer.models import GroupsList, SearchStory, DeltaParse
# Create your views here.
from django.template.context_processors import csrf


def home(request):
    group_form = GroupForm
    try:
        args ={}
        args.update(csrf(request))
        args['username'] = auth.get_user().username
        args['groups'] = GroupsList.objects.filter(author= args['username'])
        args['group_form'] = group_form
    except:
        args = {}
    return render_to_response('index.html', args)


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

def login(request):
    return None


def groupadd(request, username):
    return None


def groupdel(request):
    return None


