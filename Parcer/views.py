from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from Parcer.forms import GroupForm
from Parcer.models import GroupsList, SearchStory, DeltaParse, User
from django.template.context_processors import csrf


def home(request):
    group_form = GroupForm
    args = {}
    try:
        args.update(csrf(request))
        args['username'] = auth.get_user(request).username
        user = User.objects.get(username=args['username'])
        args['groups'] = GroupsList.objects.filter(author=user.id)
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
    auth.logout(request)
    return redirect('/')


def groupadd(request, username):
    if request.POST:
        form = GroupForm(request.POST)
        group = form.save(commit=False)
        user = User.objects.get(username=username)
        group.author = user.id
        group.save()
        form.save_m2m()
    return redirect('/')


def groupdel(request):
    return None


