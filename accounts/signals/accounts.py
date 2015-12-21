from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from ..models import UserProfile


@receiver(post_save, sender=User)
def registration_handler(sender, instance, created, **kwargs):

    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
