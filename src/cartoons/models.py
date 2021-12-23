from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

status_options = (
    ("COMPLETED", "Completed"),
    ("RELEASING", "Releasing"),
    ("PLANNED", "Planned")
)

class VoiceActor(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class Network(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.genre

class Series(models.Model):
    name = models.CharField(max_length=200)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True)
    summary = models.CharField(max_length=10000)
    season_count = models.IntegerField(default=1)
    cover_image = models.URLField(blank=True)
    background_image = models.URLField(blank=True)
    status = models.CharField(max_length=50, choices=status_options)

    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=200)
    voice_actor = models.ForeignKey(VoiceActor, on_delete=models.CASCADE)
    image = models.URLField(blank=True)
    series  = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Episode(models.Model):
    episode_number = models.IntegerField()
    absolute_episode_number = models.IntegerField()
    season_number = models.IntegerField(default=1)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=100)
    release_date = models.DateTimeField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    screenshot = models.URLField(blank=True)

    def __str__(self) -> str:
        return str(self.series) + " S" + str(self.season_number) + "E" + str(self.episode_number) + ": " + self.name