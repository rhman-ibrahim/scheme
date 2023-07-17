from django.db.models.signals import post_save
from mate.models import FriendRequest, Scheme
from django.dispatch import receiver


@receiver(post_save, sender=FriendRequest)
def reader(sender, instance, created, **kwargs):

    if int(instance.status) == 1:

        receiver = Scheme.objects.get(user=instance.receiver)
        receiver.friends.add(sender.user)
        receiver.save()

        sender   = Scheme.objects.get(user=instance.sender)
        sender.friends.add(receiver.user)
        sender.save()