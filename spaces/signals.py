from django.db.models.signals import post_save
from django.dispatch import receiver
from circles.models import Circle
from signals.models import Signal
from .models import Room


@receiver(post_save, sender=Circle)
def reader(sender, instance, created, **kwargs):
    if created:
        Room.objects.create(circle=instance, space=instance.serial)


@receiver(post_save, sender=Signal)
def reader(sender, instance, created, **kwargs):
    if created:
        Room.objects.create(circle=instance.circle, space=instance.serial)