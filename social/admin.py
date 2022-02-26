from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('date_created')

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("thought", "user", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('date_created',)