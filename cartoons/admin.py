from django.contrib import admin
from .models import Team, VoiceActor, Character, Network, Genre, Cartoon, Episode, Location

# Register your models here.
admin.site.register(Genre)

@admin.register(Cartoon)
class CartoonAdmin(admin.ModelAdmin):
    list_display = ("name", "network", "status", "rating", "date_created")

    def get_readonly_fields(self, request, obj=None): 
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'background_image', 'rating', 'date_created')
        return self.readonly_fields + ('rating', 'date_created')

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "alias", "status", "alignment", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("name", "episode_number", "season_number", "release_date", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('screenshot', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    list_display = ("name", "date_of_birth", "date_of_death", "date_created")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("base_name", "city", "nation", "date_created")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('date_created',)