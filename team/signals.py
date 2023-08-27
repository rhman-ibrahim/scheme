from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Space, Membership


@receiver(post_save, sender=Space)
def reader(sender, instance, created, **kwargs):
    if created:
        Membership.objects.create(
            user=instance.founder,
            space=instance
        )