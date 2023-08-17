# Django
# from django.contrib import auth
# from django.shortcuts import redirect
# from django.contrib.messages import constants as messages
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

# Celery
from celery import shared_task

# User
from .models import Account, Token


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
    
# @shared_task
# def deactivating_guest_user_accounts():
#     query = Account.objects.filter(is_guest=True)
#     if query.exists():
#         for guest in query.all():
#             if guest.is_expired:
#                 auth.logout(guest)
#                 guest.is_active = False
#                 guest.save()
#                 messages.add_message(
#                     guest, messages.INFO, "Your guest account has been deactivated."
#                 )
#                 return redirect("home:retrieve_home_index")
#             else:
#                 pass
#     else:
#         return 0