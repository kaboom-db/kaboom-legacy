from django.contrib import admin
from .models import VoiceActor, Character, Network, Genre, Cartoon, Episode

# Register your models here.
admin.site.register(Genre)

@admin.register(Cartoon)
class CartoonAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None): 
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'background_image', 'rating')
        return self.readonly_fields + ('rating',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image',)
        return self.readonly_fields

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('screenshot',)
        return self.readonly_fields

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo',)
        return self.readonly_fields

@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image',)
        return self.readonly_fields