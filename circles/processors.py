from circles.models import Circle


def opened_circle(request):
    circle_uuid = request.session['circle'] if 'circle' in request.session else None
    return {
        'opened_circle': Circle.objects.get(uuid=circle_uuid) if circle_uuid else None
    }