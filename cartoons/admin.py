from django.contrib import admin
from .models import Team, VoiceActor, Character, Network, Genre, Cartoon, Episode

# Register your models here.
admin.site.register(Genre)

@admin.register(Cartoon)
class CartoonAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None): 
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'background_image', 'rating', 'date_created')
        return self.readonly_fields + ('rating', 'date_created')

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('screenshot', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo', 'date_created')
        return self.readonly_fields + ('date_created',)