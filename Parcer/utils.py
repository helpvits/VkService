from django.contrib import auth
from Parcer.models import GroupsList, User
from Parcer.forms import GroupForm


def get_usr_data(request, args):
    try:
        args['user'] = auth.get_user(request)
        args['username'] = auth.get_user(request).username
        user = User.objects.get(username=args['username'])
        args['groups'] = GroupsList.objects.filter(author=user.id)
        group_form = GroupForm
        args['group_form'] = group_form
    except Exception as e:
        print(e)
    return args
