from django.contrib import admin
from Parcer.models import GroupsList, DeltaParse, SearchStory
# Register your models here.

admin.site.register([GroupsList])
admin.site.register([DeltaParse])
admin.site.register([SearchStory])