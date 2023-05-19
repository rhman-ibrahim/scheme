from .models import Circle, Radius
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Circle)
def reader(sender, instance, created, **kwargs):
    if created:
        Radius.objects.create(circle=instance)