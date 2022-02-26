from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.aggregates import Count, Sum
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from libgravatar import Gravatar
from comics import models as comic_models
from cartoons import models as cartoons_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q
from kaboom.utils import IMG_REQUEST_FIELDS, IMG_REQUEST_OPTIONS, REQUEST_STATUS, REPORT_OPTIONS
from django.core.mail import send_mail
from kaboom.db_secrets import DEFAULT_FROM_EMAIL
from django.template import loader
from django.core.exceptions import ValidationError
from django.utils import timezone

User._meta.get_field('email')._unique = True

### When a new user is created, add a token for their account.
class UserData(models.Model):
    # Keeping this for the future
    def validate_char(value):
        if '<' in value or '>' in value:
            raise ValidationError(
                'Bio cannot contain \'<\' or \'>\'',
                params={'value': value},
            )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    bio = models.TextField(blank=True, null=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create a new token
        Token.objects.create(user=instance)
        UserData.objects.create(user=instance)
        # Send an email
        html = loader.render_to_string('website/email.html', {
            'username': instance.username
        })
        send_mail("Welcome to Kaboom", "Hello " + instance.username + ", welcome to Kaboom!", DEFAULT_FROM_EMAIL, (instance.email,), html_message=html)

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
    date_created = models.DateTimeField(default=timezone.now)

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
    date_created = models.DateTimeField(default=timezone.now)

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

class Follow(models.Model):
    class Meta:
        unique_together = (('follower', 'following'),)

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def save(self, *args, **kwargs) -> None:
        if self.follower == self.following:
            return
        super(Follow, self).save(*args, **kwargs)

class ImageRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # This needs to be blankable so that the file can be deleted when a request is rejected.
    image = models.ImageField(blank=True)
    object_type = models.CharField(max_length=50, choices=IMG_REQUEST_OPTIONS)
    request_field = models.CharField(max_length=50, choices=IMG_REQUEST_FIELDS)
    object_id = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default="NONE")

    def save(self, *args, **kwargs):
        if self.image:
            ext = self.image.name.split('.')[-1]
            self.image.name = self.object_type + '_' + str(self.object_id) + '_' + self.request_field + '.' + ext
        super(ImageRequest, self).save(*args, **kwargs)

    def __str__(self):
        return "Image Request: " + self.user.username + " | " + self.object_type

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_type = models.CharField(max_length=50, choices=REPORT_OPTIONS)
    object_id = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default="NONE")
    message = models.TextField()

    def __str__(self):
        return str(self.user) + " | " + str(self.object_type) + " | " + str(self.object_id)