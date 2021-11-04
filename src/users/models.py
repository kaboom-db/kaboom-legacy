from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user(sender, instance=None, created=False, **kwargs):
#     if created:
#         # Create a new bio
#         