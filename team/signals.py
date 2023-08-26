from django.dispatch import receiver
from django.db.models.signals import post_save
from team.models import Membership
from note.models import Secret


@receiver(post_save, sender=Membership)
def reader(sender, instance, created, **kwargs):
    if created:
        Secret.objects.create(
            user=instance.user,
            space=instance.space
        )