from django.db import models
from django.db.models.base import Model

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

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField()

class Character(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    image = models.URLField()

class Series(models.Model):
    series_name = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)
    image_small = models.URLField()
    image_medium = models.URLField()
    image_large = models.URLField()

    def __str__(self) -> str:
        return self.series_name

class Issue(models.Model):
    issue_number = models.IntegerField(default=1)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    image_small = models.URLField()
    image_medium = models.URLField()
    image_large = models.URLField()

    def __str__(self) -> str:
        return str(self.series) + ' #' + str(self.issue_number)

class Staff(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, choices=position_choices)
    image = models.URLField()