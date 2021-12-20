from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

position_choices = (
    ("WRITER", "Writer"),
    ("PENCILLER", "Penciller"),
    ("COVER ARTIST", "Cover Artist"),
    ("INKER", "Inker"),
    ("VARIANT COVER ARTIST", "Variant Cover Artist"),
    ("COLORIST", "Colorist"),
    ("LETTERER", "Letterer"),
    ("DESIGNER", "Designer"),
    ("EDITOR", "Editor"),
    ("EXECUTIVE EDITOR", "Executive Editor"),
    ("EDITOR-IN-CHIEF", "Editor-in-Chief")
)

status_options = (
    ("COMPLETED", "Completed"),
    ("RELEASING", "Releasing"),
    ("PLANNED", "Planned")
)

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField()
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, choices=position_choices)
    image = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=10000)
    image = models.URLField()

    def __str__(self) -> str:
        return self.name

class Series(models.Model):
    series_name = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    year_started = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    status = models.CharField(max_length=100, choices=status_options)
    image_small = models.URLField()
    image_medium = models.URLField()
    image_large = models.URLField()

    def __str__(self) -> str:
        return self.series_name

class Format(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class Issue(models.Model):
    class Meta:
        unique_together = (('issue_number_absolute', 'series'),)

    issue_number_absolute = models.IntegerField(default=1)
    issue_number = models.CharField(max_length=10)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    characters = models.ManyToManyField(Character, blank=True)
    staff = models.ManyToManyField(Staff, blank=True)
    format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True, blank=True)
    release_date = models.DateField()
    image_small = models.URLField()
    image_medium = models.URLField()
    image_large = models.URLField()

    def __str__(self) -> str:
        return str(self.series) + ' #' + str(self.issue_number)