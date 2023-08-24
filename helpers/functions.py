import hashlib, cv2

# Contrib
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

# Utils
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str

def secret(raw_string):
    return hashlib.sha256(str(raw_string).encode()).hexdigest()

def generate_serial():
    return get_random_string(length=32)

def get_form_errors(request, form):
    [
        messages.error(request, str(error).replace("This field", str(field.name).capitalize()))
        for field in form for error in field.errors
    ]
    [
        messages.error(request, error) for error in form.non_field_errors()
    ]

def log(user_id, instance, flag, message=""):
    # Create the log entry for C_UD operations.
    LogEntry.objects.log_action(
        user_id         = user_id,
        content_type_id = ContentType.objects.get_for_model(instance).id,
        object_id       = instance.id,
        object_repr     = force_str(instance),
        action_flag     = flag,
        change_message  = message
    )