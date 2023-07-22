from team.models import Circle
from django.shortcuts import redirect
from django.contrib import messages


def opened_circle(request):
        if 'circle' in request.session:
            try:
                return {
                    'opened_circle': Circle.objects.get(id=request.session.get('circle'))
                }
            except Circle.DoesNotExist:
                messages.warning(request, "circle does not exsit")
                request.session.pop('circle')
        return {}