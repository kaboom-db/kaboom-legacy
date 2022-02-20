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

User._meta.get_field('email')._unique = True

### When a new user is created, add a token for their account.
class UserData(models.Model):
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

class Thought(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    post_content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    limit = Q(app_label='comics', model='comic') | Q(app_label='comics', model='issue') | Q(app_label='cartoons', model='cartoon') | Q(app_label='cartoons', model='episode')
    thought_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to=limit)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('thought_type', 'related_object_id')
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

class Follow(models.Model):
    class Meta:
        unique_together = (('follower', 'following'),)

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def save(self, *args, **kwargs) -> None:
        if self.follower == self.following:
            return
        super(Follow, self).save(*args, **kwargs)

class UserLikedThought(models.Model):
    class Meta:
        unique_together = (('user', 'thought'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thought = models.ForeignKey(Thought, on_delete=models.CASCADE)

@receiver(post_save, sender=UserLikedThought)
def add_num_of_likes(sender, instance=None, created=False, **kwargs):
    if created:
        num_of_likes = UserLikedThought.objects.filter(thought=instance.thought.id).aggregate(count=Count('user'))['count']
        thought = Thought.objects.get(id=instance.thought.id)
        thought.num_of_likes = num_of_likes
        thought.save()

@receiver(post_delete, sender=UserLikedThought)
def delete_num_of_likes(sender, instance=None, **kwargs):
    num_of_likes = UserLikedThought.objects.filter(thought=instance.thought.id).aggregate(count=Count('user'))['count']
    thought = Thought.objects.get(id=instance.thought.id)
    thought.num_of_likes = num_of_likes
    thought.save()

class ImageRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    object_type = models.CharField(max_length=50, choices=IMG_REQUEST_OPTIONS)
    request_field = models.CharField(max_length=50, choices=IMG_REQUEST_FIELDS)
    object_id = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default="NONE")

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