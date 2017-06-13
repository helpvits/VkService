from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from Parcer.forms import GroupForm
from Parcer.models import GroupsList, SearchStory, DeltaParse, User
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
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Пользователь не найден'
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout()
    return redirect('/')


def groupadd(request, username):
    if request.POST:
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = User.objects.get(username=username)
            form.save()
    return redirect('/')


def groupdel(request):
    return None


