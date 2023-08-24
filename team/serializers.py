from rest_framework import serializers

from user.serializers import UsernameField
from .models import Space


class SpaceSerializer(serializers.ModelSerializer):
    founder = serializers.StringRelatedField()
    members = UsernameField(many=True)
    class Meta:
        model  = Space
        fields = ['founder', 'name', 'serial', 'members']


class SpacePostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Space
        fields = ['founder', 'name', 'password']