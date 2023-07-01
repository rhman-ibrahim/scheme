from django.db.models.signals import post_save
from django.dispatch import receiver
from circles.models import Circle
from signals.models import Signal
from .models import Room


@receiver(post_save, sender=Circle)
@receiver(post_save, sender=Signal)
def circle_room(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Circle):
            circle   = instance
        if isinstance(instance, Signal):
            circle   = instance.circle
        room = Room.objects.create(circle=circle, space=instance.serial)
        room.members.set([circle.founder, *circle.members.all()])