import os
import django
import vk


def start_parcing():
    from Parcer.models import GroupsList
    vk_api = get_api()
    try:
        groups = GroupsList.objects.all()
        group_list = []
        for group in groups:
            group_list.append(group.link)
        print(group_list)
        for group in group_list:
            get_grop_info(group, vk_api)
    except Exception as e:
        print(e)


def get_api():
    try:
        session = vk.Session()
        vk_api = vk.API(session)
        return vk_api
    except Exception as e:
        print(e)

def get_grop_info(group, vk_api):
    try:
        print(vk_api.groups.getMembers(group_id=group))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroupParcer.settings")
    django.setup()
    start_parcing()