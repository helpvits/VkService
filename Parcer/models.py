from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class GroupsList(models.Model):
    link = models.CharField(max_length=200, verbose_name='Сылка группы')
    author = models.ManyToManyField(User)


class SearchStory(models.Model):
    group_id = models.ForeignKey(GroupsList)
    parsing_date = models.DateTimeField()
    users = models.TextField()

class DeltaParse(models.Model):
    group_id = models.ForeignKey(GroupsList)
    delta_date = models.DateTimeField()