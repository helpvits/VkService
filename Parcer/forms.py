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
                self.add_error('link', 'В группе нет участников')
                raise ValidationError('В группе нет участников')
            elif info['count'] > 10000:
                self.add_error('link', 'Слишком нмого участников >10000')
                raise ValidationError('Слишком нмого участников >10000')
        else:
            self.add_error('link', 'Проблема с получением данных')
            raise ValidationError('Проблема с получением данных')
        return self.cleaned_data
