from rest_framework import status, viewsets
from dapi.serializers.home import WidgetSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dapi.decoratores import resource
from home.models import Widget

class WidgetViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    @resource
    def by_view(self, request, view):
        query = Widget.objects.filter(view=view)
        notes = {}
        for item in query.all(): notes[item.note] = item.card
        return Response(
            notes,
            status=status.HTTP_200_OK
        )
    
    @resource
    def by_name(self, request, name):
        query = Widget.objects.filter(name=name)
        return Response(
            {'notes': WidgetSerializer(query, many=True).data},
            status=status.HTTP_200_OK
        )
    
    @resource
    def by_note(self, request, name, note):
        query = Widget.objects.filter(note=note, name=name)
        return Response(
            WidgetSerializer(query, many=True).data,
            status=status.HTTP_200_OK
        )