from celery import shared_task

from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from .models import Token


@shared_task
def fixing_tokens_uuid_values():
    if Token.objects.count() != Token.objects.filter(ready=True).count():
        for token in Token.objects.all():
            try:
                token.validate_unique()
                token.value = get_random_string(length=32)
                token.ready = True
                token.save()
            except ValidationError as error:
                token.save()
    else:
        return 0