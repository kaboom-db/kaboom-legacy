from django.db import models
from django.db.models.base import Model

# Create your models here.
class Series(models.Model):
    series_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.series_name

class Issue(models.Model):
    issue_number = models.IntegerField(default=1)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.series) + ' #' + str(self.issue_number)
