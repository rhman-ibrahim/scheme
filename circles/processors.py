from circles.models import Circle
from django.shortcuts import redirect
from django.contrib import messages


def opened_circle(request):
        try:
            session = True if 'circle' in request.session else False
            serial  = request.session.get('circle') if session else None 
            circle  = Circle.objects.get(uuid=serial) if serial else None
        except Circle.DoesNotExist:
            request.session.pop('circle')
            messages.warning(request, "circle does not exsit")
            return redirect('user:navigate')
        return {
            'opened_circle': circle
        }