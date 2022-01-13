from django.contrib import admin
from . import models
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect

# Register your models here.
admin.site.register(models.ComicSubscription)
admin.site.register(models.ReadIssue)
admin.site.register(models.CartoonSubscription)
admin.site.register(models.WatchedEpisode)
admin.site.register(models.Thought)
admin.site.register(models.Comment)
admin.site.register(models.Follow)
admin.site.register(models.UserLikedThought)
#admin.site.register(models.ImageRequest)

@admin.register(models.ImageRequest)
class ImageRequestAdmin(admin.ModelAdmin):
    change_form_template = "users/image_request.html"

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