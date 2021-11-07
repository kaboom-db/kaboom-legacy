from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ComicSubscription)
admin.site.register(models.ReadIssue)