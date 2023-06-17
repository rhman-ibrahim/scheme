from rest_framework import serializers
from user.models import Account
from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.StringRelatedField()

    class Meta:
        model  = Message
        fields = ['sender', 'body']