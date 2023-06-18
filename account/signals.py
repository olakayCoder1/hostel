from django.db.models.signals import post_save 
from django.dispatch import receiver
from uuid import uuid4
from .models import (
    User , Profile
)
import os

@receiver(post_save , sender=User)
def user_profile_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"public_key_"+str(uuid4())
        instance.save()
        Profile.objects.create(user=instance)


