from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mate.models import FriendRequest
from team.models import Space
from .models import Room


@receiver(post_save, sender=FriendRequest)
def ping_room(sender, instance, **kwargs):
    if instance.status == 1:
        room, created = Room.objects.get_or_create(identifier=instance.identifier)
        room.members.set([instance.receiver, instance.sender])
        room.description = f"{instance.receiver.username} & {instance.sender.username} chat room."
        room.save()

@receiver(post_delete, sender=FriendRequest)
def ping_room(sender, instance, **kwargs):
    query = Room.objects.filter(identifier=instance.identifier)
    if query.exists():
        room = query.first()
        room.delete()

@receiver(post_save, sender=Space)
def ping_room(sender, instance, created, **kwargs):
    room, created = Room.objects.get_or_create(identifier=instance.identifier)
    room.members.set([instance.founder, *instance.members.all()])
    room.description = f"{instance.name} circle's chat room, {room.members.count()} of {instance.members.count()} are in."
    room.save()