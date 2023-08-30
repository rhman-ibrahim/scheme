from team.models import Space


def space(request):
    if 'space' in request.session:
        try:
            return {
                'space': Space.objects.get(id=request.session.get('space'))
            }
        except Space.DoesNotExist:
            request.session.pop('circle')
    return {}