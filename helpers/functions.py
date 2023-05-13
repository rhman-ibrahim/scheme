from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.utils.encoding import force_str


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

def get_form_errors(request, form):
    [messages.error(request, error) for field in form for error in field.errors]
    [messages.error(request, error) for error in form.non_field_errors()]

def completion(fields):
    incomplete = 0
    if any(field is None or field == '' for field in fields) is True:
        incomplete += 1
    return round((len(fields) - incomplete) / len(fields), 2)
