from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from kaboom.utils import STATUS_OPTIONS

class VoiceActor(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(VoiceActor, self).save(*args, **kwargs)

class Network(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.URLField(blank=True, max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Network, self).save(*args, **kwargs)

class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.genre

class Character(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, null=True, blank=True)
    voice_actors = models.ManyToManyField(VoiceActor, blank=True)
    image = models.URLField(blank=True, max_length=500)
    biography = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Character, self).save(*args, **kwargs)

class Cartoon(models.Model):
    name = models.CharField(max_length=200)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    summary = models.TextField(blank=True)
    season_count = models.IntegerField(default=1)
    cover_image = models.URLField(blank=True, max_length=500)
    background_image = models.URLField(blank=True, max_length=500)
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    characters = models.ManyToManyField(Character, blank=True)
    website = models.URLField(blank=True, null=True)
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    tmdb_id = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Cartoon, self).save(*args, **kwargs)

class Episode(models.Model):
    class Meta:
        unique_together = (('episode_number', 'season_number', 'series'))

    episode_number = models.IntegerField()
    season_number = models.IntegerField(default=1)
    series = models.ForeignKey(Cartoon, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    screenshot = models.URLField(blank=True, max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    runtime = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.series) + " S" + str(self.season_number) + "E" + str(self.episode_number) + ": " + self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Episode, self).save(*args, **kwargs)