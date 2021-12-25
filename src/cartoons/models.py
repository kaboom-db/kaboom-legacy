from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.aggregates import Count, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from kaboom.utils import util_calculate_age, STATUS_OPTIONS

class VoiceActor(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

@receiver(pre_save, sender=VoiceActor)
def calculate_age(sender, instance=None, created=False, **kwargs):
    today = date.today()
    if instance.date_of_birth:
        if instance.date_of_death:
            instance.age = util_calculate_age(instance.date_of_birth, instance.date_of_death)
        else:
            instance.age = util_calculate_age(instance.date_of_birth, today)
    else:
        instance.age = None

class Network(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.genre

class Character(models.Model):
    name = models.CharField(max_length=200)
    voice_actor = models.ForeignKey(VoiceActor, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.URLField(blank=True)
    biography = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class Cartoon(models.Model):
    name = models.CharField(max_length=200)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    summary = models.TextField(blank=True)
    season_count = models.IntegerField(default=1)
    cover_image = models.URLField(blank=True)
    background_image = models.URLField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True)
    characters = models.ManyToManyField(Character, blank=True)

    def __str__(self) -> str:
        return self.name

class Episode(models.Model):
    episode_number = models.IntegerField()
    absolute_episode_number = models.IntegerField()
    season_number = models.IntegerField(default=1)
    series = models.ForeignKey(Cartoon, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    release_date = models.DateTimeField()
    screenshot = models.URLField(blank=True)

    def __str__(self) -> str:
        return str(self.series) + " S" + str(self.season_number) + "E" + str(self.episode_number) + ": " + self.name