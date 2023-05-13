from user.models import Account, Token, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Account)
def reader(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)