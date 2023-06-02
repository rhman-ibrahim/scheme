import uuid

from django.contrib.auth import authenticate, login
from django.contrib.admin.models import CHANGE

from helpers.functions import log

from user.models import Account


def create_a_guest_user(request):

    uuid_key_8 = str(uuid.uuid4())[:8]
    uuid_key16 = str(uuid.uuid4())[:16]
    
    Account.objects.create_lazy_user(
        username=uuid_key_8,
        password=uuid_key16
    )
    user = authenticate(
        username=uuid_key_8,
        password=uuid_key16
    )
    
    if user is not None:
        login(request, user)
        log(
            request.user.id,
            request.user,
            CHANGE,
            "signed in as a user"
        )
