import datetime, timeago
from django.utils.timezone import utc
from django import template

from user.models import Account

register = template.Library()

# Message
@register.filter
def message(tag, prop):
    tags = {
        "error": {
            'color':'danger-background',
            'icon':'error'
        },
        "info": {
            'color':'info-background',
            'icon':'info'
        },
        "warning": {
            'color':'warning-background',
            'icon':'warning'
        },
        "success": {
            'color':'success-background',
            'icon':'done'
        },
    }
    tag_props = tags.get(tag, {})
    return tag_props.get(prop, '')

@register.filter
def space_friends(account, space):
    friends = [int(friend.id) for friend in account.profile.friends.all()]
    members = [int(member.id) for member in space.members.all()]
    return Account.objects.filter(pk__in=list(set(members).intersection(set(friends))))

# Model
@register.filter
def get_class(value):
    return value.__class__.__name__

# Time
@register.filter
def ago(time_stamp):
    if isinstance(time_stamp, datetime.datetime):
        return timeago.format(time_stamp, datetime.datetime.utcnow().replace(tzinfo=utc))
    return "---"

# Numbers
@register.filter
def float_to_percentage(fraction):
    if isinstance(fraction, float): return f"{int(fraction * 100)}%"
    return fraction

# Strings
@register.filter
def replace_underscores(text):
    return str(text).replace("_", " ").title()

# Logs
@register.filter
def flag_repr(index):
    flags = {
        "1":"add",
        "2":"change",
        "3":"delete"
    }
    return flags[f'{index}']