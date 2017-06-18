from django.http import HttpResponseRedirect
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
    except Exception as e:
        print(e)
    return render_to_response('index.html', args)


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
    return redirect('/')


def group_add(request, username):
    if request.POST:
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
            form = GroupForm()
            request.session.modified = True
    return render(request, 'index.html', {'form': form})


def group_del(request, username, group_id):
    try:
        group = GroupsList.objects.get(link=group_id)
        user = User.objects.get(username=username)
        group.author.remove(user.id)
    except:
        redirect('/')
    return redirect('/')


def make_delta(request):
    return None