from django import template
from django.conf import settings

register = template.Library()

@register.filter
def profile_picture_url(user):
    if hasattr(user, 'profile') and user.profile.picture:
        return user.profile.picture.url
    return settings.DEFAULT_PROFILE_PICTURE_URL