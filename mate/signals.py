from django.dispatch import receiver
from django.db.models.signals import post_save
from mate.models import FriendRequest, Profile


@receiver(post_save, sender=FriendRequest)
def reader(sender, instance, created, **kwargs):

    if int(instance.status) == 1:

        receiver = Profile.objects.get(user=instance.receiver)
        sender   = Profile.objects.get(user=instance.sender)

        receiver.friends.add(sender.user)
        sender.friends.add(receiver.user)
        
        receiver.save()
        sender.save()