from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Thought(models.Model):
    THOUGHT_TYPES = (
        ('COMIC', 'Comic'),
        ('ISSUE', 'Issue'),
        ('CARTOON', 'Cartoon'),
        ('EPISODE', 'Episode')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    post_content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    thought_type = models.CharField(max_length=10, choices=THOUGHT_TYPES, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
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