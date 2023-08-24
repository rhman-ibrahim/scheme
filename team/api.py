# REST
from rest_framework.response import Response
from rest_framework import status, viewsets

# Helpers
from helpers.functions import secret
from dapi.decoratores import resource

# Dapi
from .serializers import (
    SpaceSerializer, SpacePostSerializer
)

# Team
from .models import Space


class SpaceViewSet(viewsets.ViewSet):

    @resource
    def info(self, request, pk=None):
        return Response(
            SpaceSerializer(Space.objects.get(id=pk)).data,
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        serializer = SpacePostSerializer(
            data = {
                "password": secret(request.POST.get('password')) if bool(request.POST.get('password')) else None,
                "name": request.POST.get('name'),
                "founder": request.user.id,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )