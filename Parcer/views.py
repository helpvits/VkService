from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from Parcer.forms import GroupForm
from Parcer.models import GroupsList, SearchStory, DeltaParse, User
from django.template.context_processors import csrf
from Parcer.GroupParce import get_api, get_grop_info, insert_group_info



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


def group_add(request, username):
    if request.POST:
        user = User.objects.get(username=username)
        form = GroupForm(request.POST)
        input_group = form.save(commit=False)
        group_link = input_group.link
        group_info = get_grop_info(input_group.link, get_api())
        if group_info['count'] < 0:
            err = 'No group info'
        elif group_info['count'] > 10000:
            err = 'So many people'
        else:
            try:
                group = GroupsList.objects.get(link=group_link)
                group.author.add(user.id)
            except:
                input_group = form.save()
                group_link = input_group.link
                group = GroupsList.objects.get(link=group_link)
                group.author.add(user.id)
                insert_group_info(input_group.link, group_info['users'])
        #group.save()
        #form.save_m2m()
    return redirect('/')


def group_del(request, username, group_id):
    try:
        group = GroupsList.objects.get(link=group_id)
        user = User.objects.get(username=username)
        group.author.remove(user.id)
    except:
        redirect('/')
    return redirect('/')


