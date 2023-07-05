from django.db.models.signals import post_save
from django.dispatch import receiver
from team.models import Circle
from blog.models import Signal
from .models import Room


@receiver(post_save, sender=Circle)
def circle_room(sender, instance, created, **kwargs):
    if created:
        Room.objects.create(circle=instance, serial=instance.serial)
    room = Room.objects.get(serial=instance.serial)
    room.members.set([instance.founder, *instance.members.all()])
    print([instance.founder, *instance.members.all()])

@receiver(post_save, sender=Signal)
def circle_room(sender, instance, created, **kwargs):
    if created:
        Room.objects.create(circle=instance.circle, serial=instance.serial)
    room = Room.objects.get(serial=instance.serial)
    room.members.set([instance.circle.founder, *instance.circle.members.all()])
    print([instance.circle.founder, *instance.circle.members.all()])