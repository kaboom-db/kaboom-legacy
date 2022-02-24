from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "num_of_likes", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('num_of_likes', 'date_created')

@admin.register(models.UserLikedThought)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("thought", "user")

@admin.register(models.Comment)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("thought", "user", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('date_created',)