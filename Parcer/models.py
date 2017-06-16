from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class GroupsList(models.Model):
    link = models.CharField(max_length=200, verbose_name='Сылка группы')
    author = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Список групп'
        verbose_name_plural = 'Список групп'

    def __str__(self):
        return self.link

class SearchStory(models.Model):
    group_id = models.ForeignKey(GroupsList)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.TextField()
    users_count = models.CharField(max_length=200, verbose_name='количество участников', null=True, blank=True)

    class Meta:
        verbose_name = 'История проверок'
        verbose_name_plural = 'История проверок'

    def __str__(self):
        return str(self.group_id)


class DeltaParse(models.Model):
    group_id = models.ForeignKey(GroupsList)
    delta_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Дельты'
        verbose_name_plural = 'Дельты'

    def __str__(self):
        return self.group_id

