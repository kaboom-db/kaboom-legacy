from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.aggregates import Count, Sum
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
    
    series = models.ForeignKey(comic_models.Comic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self) -> str:
        return "Comic: " + str(self.series) + ", User: " + str(self.user)

@receiver(post_save, sender=ComicSubscription)
def add_ratings_comicsubs(sender, instance=None, created=False, **kwargs):
    if instance.rating:
        count = ComicSubscription.objects.filter(series=instance.series).aggregate(count=Count('rating'))['count']
        sum = ComicSubscription.objects.filter(series=instance.series).aggregate(sum=Sum('rating'))['sum']
        avg = sum / count
        s = comic_models.Comic.objects.get(id=instance.series.id)
        s.rating = avg
        s.save()

class ReadIssue(models.Model):
    issue = models.ForeignKey(comic_models.Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "Issue: " + str(self.issue) + ", User: " + str(self.user) + ", Read: " + str(self.read_at)

class CartoonSubscription(models.Model):
    class Meta:
        unique_together = (('series', 'user'),)
    
    series = models.ForeignKey(cartoons_models.Cartoon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self) -> str:
        return "Cartoon: " + str(self.series) + ", User: " + str(self.user)

@receiver(post_save, sender=CartoonSubscription)
def add_ratings_cartoonsubs(sender, instance=None, created=False, **kwargs):
    if instance.rating:
        # Calculate the rating for a comic series
        count = CartoonSubscription.objects.filter(series=instance.series).aggregate(count=Count('rating'))['count']
        sum = CartoonSubscription.objects.filter(series=instance.series).aggregate(sum=Sum('rating'))['sum']
        avg = sum / count
        s = cartoons_models.Cartoon.objects.get(id=instance.series.id)
        s.rating = avg
        s.save()
        print(s.rating)

class WatchedEpisode(models.Model):
    episode = models.ForeignKey(cartoons_models.Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "Episode: " + str(self.episode) + ", User: " + str(self.user) + ", Watched: " + str(self.watched_at)

class ThoughtType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name

class Thought(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    post_content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    thought_type = models.ForeignKey(ThoughtType, blank=True, null=True, on_delete=models.SET_NULL)
    comic = models.ForeignKey(comic_models.Comic, blank=True, null=True, on_delete=models.SET_NULL)
    issue = models.ForeignKey(comic_models.Issue, blank=True, null=True, on_delete=models.SET_NULL)
    cartoon = models.ForeignKey(cartoons_models.Cartoon, blank=True, null=True, on_delete=models.SET_NULL)
    episode = models.ForeignKey(cartoons_models.Episode, blank=True, null=True, on_delete=models.SET_NULL)
    num_of_likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    thought = models.ForeignKey(Thought, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Comment on: " + str(self.thought) + ", User: " + str(self.user)