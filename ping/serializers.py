from rest_framework import serializers
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    class Meta:
        model  = Message
        fields = ['sender', 'body']


class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model  = Room
        fields = "__all__"