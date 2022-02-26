from django.db import models
from django.contrib.auth.models import User
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

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    thought = models.ForeignKey(Thought, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Comment on: " + str(self.thought) + ", User: " + str(self.user)