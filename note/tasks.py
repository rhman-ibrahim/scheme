from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

# Celery
from celery import shared_task

# User
from user.models import Token
from team.models import Membership

@shared_task
def fixing_tokens_keys():
    if Token.objects.count() != Token.objects.filter(ready=True).count():
        for token in Token.objects.all():
            try:
                token.validate_unique()
                token.key = get_random_string(length=32)
                token.ready = True
                token.save()
            except ValidationError as error:
                token.save()
    else:
        return 0

@shared_task
def fixing_memberships_keys():
    if Membership.objects.count() != Membership.objects.filter(ready=True).count():
        for membership in Membership.objects.all():
            try:
                membership.validate_unique()
                membership.key = get_random_string(length=32)
                membership.ready = True
                membership.save()
            except ValidationError as error:
                membership.save()
    else:
        return 0