from team.models import Space
from django.shortcuts import redirect
from django.contrib import messages


def opened_space(request):
        if 'circle' in request.session:
            try:
                return {
                    'opened_space': Space.objects.get(id=request.session.get('circle'))
                }
            except Space.DoesNotExist:
                messages.warning(request, "space does not exsit")
                request.session.pop('circle')
        return {}