from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.utils.text import slugify
from uuid import uuid4
from .models import (
     Hostel , Compound , Room ,
    Document, Booking
)
import os



@receiver(post_save , sender=Hostel)
def hostel_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = "hostel_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Compound)
def compound_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = "compound_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Room)
def room_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = "room_"+str(uuid4())
        instance.save()



@receiver(post_save , sender=Document)
def document_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = "doc_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Booking)
def booking_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = "book_"+str(uuid4())
        instance.save()