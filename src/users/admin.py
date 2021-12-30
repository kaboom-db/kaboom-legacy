from django.contrib import admin
from . import models
from django.contrib.contenttypes.models import ContentType

# Register your models here.
admin.site.register(models.ComicSubscription)
admin.site.register(models.ReadIssue)
admin.site.register(models.CartoonSubscription)
admin.site.register(models.WatchedEpisode)
admin.site.register(models.Thought)
# admin.site.register(models.ThoughtType)
admin.site.register(models.Comment)
admin.site.register(models.Follow)
admin.site.register(models.UserLikedThought)
admin.site.register(ContentType)