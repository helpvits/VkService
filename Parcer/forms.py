from django.forms import ModelForm, ValidationError
from Parcer.models import GroupsList
from Parcer.GroupParce import get_api, get_grop_info


class GroupForm(ModelForm):
    class Meta:
        model = GroupsList
        fields = ['link']

    def clean(self):
        link = self.cleaned_data.get('link')
        vk_api = get_api()
        info = get_grop_info(link, vk_api)
        if info['count']:
            if info['count'] < 0:
                raise ValidationError('В группе нет участников')
            elif info['count'] > 10000:
                raise ValidationError('Слишком нмого участников >10000')
        else:
            raise ValidationError('Проблема с получением данных')
        return self.cleaned_data
