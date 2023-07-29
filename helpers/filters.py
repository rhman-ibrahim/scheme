import datetime, timeago
from datetime import datetime as stamp
from django.utils.timezone import utc
from django import template


register = template.Library()

# Message
@register.filter
def message(tag, prop):

    tags = {
        "error": {
            'background':'danger-background',
            'icon':'error'
        },
        "info": {
            'background':'info-background',
            'icon':'info'
        },
        "warning": {
            'background':'warning-background',
            'icon':'warning'
        },
        "success": {
            'background':'success-background',
            'icon':'done'
        },
    }

    tag_props = tags.get(tag, {})
    return tag_props.get(prop, '')


# Model
@register.filter
def get_class(value):
    return value.__class__.__name__

# Time
@register.filter
def ago(time_stamp):
    if isinstance(time_stamp, stamp):
        return timeago.format(time_stamp, datetime.datetime.utcnow().replace(tzinfo=utc))
    return "---"
@register.filter
def ago_shorten(time_stamp):
    if isinstance(time_stamp, stamp):
        statment = str(timeago.format(time_stamp, datetime.datetime.utcnow().replace(tzinfo=utc)))
        if "second" in statment:
            return statment.replace("second", "sec")
        if "minute" in statment:
            return statment.replace("minute", "min")
        if "month" in statment:
            return statment.replace("month", "mth")
        if "week" in statment:
            return statment.replace("week", "wk")
        if "year" in statment:
            return statment.replace("year", "yr")
        if "hour" in statment:
            return statment.replace("hour", "hr")
        if "day" in statment:
            return statment.replace("day", "dy")
    return statment

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