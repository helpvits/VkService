from django.contrib import admin
from Parcer.models import GroupsList, DeltaParse, SearchStory
# Register your models here.

admin.site.register([GroupsList, DeltaParse, SearchStory])
