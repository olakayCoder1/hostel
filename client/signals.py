from django.db.models.signals import post_save 
from django.dispatch import receiver
from uuid import uuid4
from .models import (
    HostelCategory, Hostel , Compound , Room ,
    Document, Booking
)
import os



@receiver(post_save , sender=HostelCategory)
def hostel_category_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"hl_cat_"+str(uuid4())
        instance.save()




@receiver(post_save , sender=Hostel)
def hostel_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"hl_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Compound)
def compound_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"cd_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Room)
def room_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"rm_"+str(uuid4())
        instance.save()



@receiver(post_save , sender=Document)
def document_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"doc_"+str(uuid4())
        instance.save()


@receiver(post_save , sender=Booking)
def booking_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = f"bk_"+str(uuid4())
        instance.save()