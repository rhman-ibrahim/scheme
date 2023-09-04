from rest_framework import serializers
from team.models import Space
from .user import UsernameField


class SpaceSerializer(serializers.ModelSerializer):
    founder = serializers.StringRelatedField()
    members = UsernameField(many=True)
    class Meta:
        model  = Space
        fields = ['founder', 'name', 'identifier', 'members']


class SpacePostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Space
        fields = ['founder', 'name', 'password']