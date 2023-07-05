from django import template
from user.models import Account


register = template.Library()

@register.filter
def user_role(circle, user_id):
    user = Account.objects.get(id=user_id)
    return circle.user_role(user)