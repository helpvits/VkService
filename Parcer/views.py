from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from Parcer.forms import GroupForm
from Parcer.models import GroupsList, SearchStory, DeltaParse, User
from django.template.context_processors import csrf
from Parcer.GroupParce import get_api, get_grop_info, insert_group_info
from Parcer.utils import get_usr_data


def home(request):
    try:
        if auth.get_user(request).username:
            args = {}
            try:
                args.update(csrf(request))
                get_usr_data(request, args)
                return render_to_response('index.html', args)
            except Exception as e:
                print(e)
        else:
            return redirect('/login/')
    except Exception as e:
        print(e)


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            new_user = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, new_user)
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
    return redirect('/login/')


def group_add(request):
    if request.POST:
        username = auth.get_user(request).username
        args = {}
        user = User.objects.get(username=username)
        form = GroupForm(request.POST)
        if form.is_valid():
            input_group = form.save(commit=False)
            group_link = input_group.link
            group_info = get_grop_info(input_group.link, get_api())
            try:
                group = GroupsList.objects.get(link=group_link)
                try:
                    group.author.add(user.id)
                except Exception as e:
                    print(e)
                insert_group_info(input_group.link, group_info)
            except:
                input_group = form.save()
                group_link = input_group.link
                group = GroupsList.objects.get(link=group_link)
                group.author.add(user.id)
                insert_group_info(input_group.link, group_info)
        else:
            args.update(csrf(request))
            args = get_usr_data(request, args)
            return render(request, 'index.html', args)
    return HttpResponseRedirect('/', args)


def group_del(request, group_id):
    try:
        username = auth.get_user(request).username
        group = GroupsList.objects.get(link=group_id)
        user = User.objects.get(username=username)
        group.author.remove(user.id)
    except:
        redirect('/')
    return redirect('/')


def make_delta(request):
    return None