from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone
from kaboom.utils import util_calculate_age, STATUS_OPTIONS

# Create your models here.
class StaffPositions(models.Model):
    position = models.CharField(max_length=250, unique=True)
    
    def __str__(self) -> str:
        return self.position

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True, max_length=500)
    website = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Publisher, self).save(*args, **kwargs)

class Staff(models.Model):
    name = models.CharField(max_length=200)
    position = models.ForeignKey(StaffPositions, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.URLField(blank=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    biography = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Staff, self).save(*args, **kwargs)

@receiver(pre_save, sender=Staff)
def calculate_age(sender, instance=None, created=False, **kwargs):
    today = date.today()
    if instance.date_of_birth:
        if instance.date_of_death:
            instance.age = util_calculate_age(instance.date_of_birth, instance.date_of_death)
        else:
            instance.age = util_calculate_age(instance.date_of_birth, today)
    else:
        instance.age = None

class Character(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, null=True, blank=True)
    image = models.URLField(blank=True, max_length=500)
    biography = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Character, self).save(*args, **kwargs)

class Comic(models.Model):
    series_name = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
    summary = models.TextField(blank=True)
    year_started = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)
    cover_image = models.URLField(blank=True, max_length=500)
    background_image = models.URLField(blank=True, max_length=500)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.series_name

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Comic, self).save(*args, **kwargs)

class Format(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.name

class Issue(models.Model):
    class Meta:
        unique_together = (('issue_number_absolute', 'series'),)

    issue_number_absolute = models.IntegerField(default=1)
    issue_number = models.CharField(max_length=10)
    series = models.ForeignKey(Comic, on_delete=models.CASCADE)
    summary = models.TextField(blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    staff = models.ManyToManyField(Staff, blank=True)
    format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)
    cover_image = models.URLField(blank=True, max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.series) + ' #' + str(self.issue_number)

    def save(self, *args, **kwargs) -> None:
        self.date_created = timezone.now()
        super(Issue, self).save(*args, **kwargs)