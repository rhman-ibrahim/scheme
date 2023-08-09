from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mate.models import FriendRequest
from team.models import Circle
from blog.models import Post
from .models import Room


@receiver(post_save, sender=FriendRequest)
def ping_room(sender, instance, **kwargs):
    if instance.status == 1:
        room, created = Room.objects.get_or_create(serial=instance.serial)
        room.members.set([instance.receiver, instance.sender])

@receiver(post_delete, sender=FriendRequest)
def ping_room(sender, instance, **kwargs):
    query = Room.objects.filter(serial=instance.serial)
    if query.exists():
        room = query.first()
        room.delete()

@receiver(post_save, sender=Circle)
def ping_room(sender, instance, created, **kwargs):
    room, created = Room.objects.get_or_create(serial=instance.serial)
    room.members.set([instance.founder, *instance.members.all()])

@receiver(post_save, sender=Post)
def ping_room(sender, instance, created, **kwargs):
    room, created = Room.objects.get_or_create(serial=instance.serial)
    room.members.set([instance.circle.founder, *instance.circle.members.all()])