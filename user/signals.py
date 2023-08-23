from django.dispatch import receiver
from django.db.models.signals import post_save
from user.models import Account, Token, Profile


@receiver(post_save, sender=Account)
def reader(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)