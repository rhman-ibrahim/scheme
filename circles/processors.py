from circles.models import Circle


def opened_circle(request):
    circle_id = request.session['circle'] if 'circle' in request.session else None
    circle    = Circle.objects.get(id=circle_id) if circle_id else None
    return {
        'opened_circle': circle
    }