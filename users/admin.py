from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect

# Register your models here.
class UserDataInline(admin.StackedInline):
    model = models.UserData
    can_delete = False
    verbose_name_plural = 'user data'

class UserAdmin(BaseUserAdmin):
    inlines = (UserDataInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(models.Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "num_of_likes", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('num_of_likes', 'date_created')

@admin.register(models.Comment)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("thought", "user", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('date_created',)

@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following")

@admin.register(models.ComicSubscription)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("series", "user", "rating")

@admin.register(models.ReadIssue)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("issue", "user", "read_at")

@admin.register(models.CartoonSubscription)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("series", "user", "rating")

@admin.register(models.WatchedEpisode)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("episode", "user", "watched_at")

@admin.register(models.UserLikedThought)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("thought", "user")

@admin.register(models.Report)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "object_type", "object_id", "status")

@admin.register(models.ImageRequest)
class ImageRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "object_type", "request_field", "object_id", "status")
    change_form_template = "users/image_request.html"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'image', 'object_type', 'request_field', 'object_id', 'status')
        return self.readonly_fields

    def response_change(self, request, obj):
        if '_approve' in request.POST:
            if obj.status == 'NONE':
                # Approve the request
                # Get the model
                str_app = obj.object_type.split('_')[0]
                str_model = obj.object_type.split('_')[1]
                field = obj.request_field
                model_class = apps.get_model(str_app.lower(), str_model.lower())
                # Get the object
                try:
                    o = model_class.objects.get(id=obj.object_id)
                    # We need to figure out what field needs to be updated
                    if field == 'COVER':
                        # This is a cover_image
                        if hasattr(o, 'cover_image'):
                            o.cover_image = obj.image.url
                            o.save()
                            obj.status = 'ACCEPTED'
                            obj.save()
                        else:
                            raise BaseException('No attribute cover')
                    elif field == 'BACKGROUND':
                        if hasattr(o, 'background_image'):
                            o.background_image = obj.image.url
                            o.save()
                            obj.status = 'ACCEPTED'
                            obj.save()
                        else:
                            raise BaseException('No attribute background')
                    elif field == 'GENERIC':
                        if hasattr(o, 'image'):
                            o.image = obj.image.url
                            o.save()
                            obj.status = 'ACCEPTED'
                            obj.save()
                        else:
                            raise BaseException('No attribute image')
                    elif field == 'LOGO':
                        if hasattr(o, 'logo'):
                            o.logo = obj.image.url
                            o.save()
                            obj.status = 'ACCEPTED'
                            obj.save()
                        else:
                            raise BaseException('No attribute logo')
                    elif field == 'SCREENSHOT':
                        if hasattr(o, 'screenshot'):
                            o.screenshot = obj.image.url
                            o.save()
                            obj.status = 'ACCEPTED'
                            obj.save()
                        else:
                            raise BaseException('No attribute screenshot')
                    self.message_user(request, 'This request has now been approved')
                except BaseException as e:
                    print(str(e))
                    self.message_user(request, 'Could not accept request. See error: ' + str(e), messages.ERROR)
                    return HttpResponseRedirect('.')
            else:
                self.message_user(request, 'Request has already been ' + obj.status.lower(), messages.ERROR)
                return HttpResponseRedirect('.')
        elif '_reject' in request.POST:
            if obj.status == "NONE":
                # Reject the request
                # Delete the file
                obj.image.delete()
                obj.status = 'REJECTED'
                obj.save()
                self.message_user(request, 'This request has now been rejected')
            else:
                self.message_user(request, 'Request has already been ' + obj.status.lower(), messages.ERROR)
                return HttpResponseRedirect('.')
        return super().response_change(request, obj)