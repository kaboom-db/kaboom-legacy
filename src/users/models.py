from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from libgravatar import Gravatar
from comics import models as comic_models
from cartoons import models as cartoons_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

### When a new user is created, add a token for their account.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create a new token
        Token.objects.create(user=instance)

def get_user_image(email) -> str:
    g = Gravatar(email)
    image = g.get_image(default='retro')
    return image

class ComicSubscription(models.Model):
    class Meta:
        unique_together = (('series', 'user'),)
    
    series = models.ForeignKey(comic_models.Series, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

class ReadIssue(models.Model):
    issue = models.ForeignKey(comic_models.Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(default=timezone.now)

class CartoonSubscription(models.Model):
    class Meta:
        unique_together = (('series', 'user'),)
    
    series = models.ForeignKey(cartoons_models.Series, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

class WatchedEpisode(models.Model):
    episode = models.ForeignKey(cartoons_models.Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(default=timezone.now)