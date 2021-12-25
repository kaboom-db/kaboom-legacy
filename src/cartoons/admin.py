from django.contrib import admin
from .models import VoiceActor, Character, Network, Genre, Cartoon, Episode

# Register your models here.
admin.site.register(VoiceActor)
admin.site.register(Character)
admin.site.register(Network)
admin.site.register(Genre)
admin.site.register(Cartoon)
admin.site.register(Episode)