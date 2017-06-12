from django.forms import ModelForm
from Parcer.models import GroupsList


class GroupForm(ModelForm):
    class Meta:
        model = GroupsList
        fields = ['link']