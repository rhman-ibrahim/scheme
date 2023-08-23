from rest_framework import serializers
from user.models import Account
from ping.models import Room, Message
from team.models import Space


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Account
        fields = ('username',)

class UsernameField(serializers.RelatedField):
     
    queryset = Account.objects.all()

    def to_representation(self, value):
        return value.username


class SpacePostSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Space
        fields = ['founder', 'name', 'password']

class SpaceSerializer(serializers.ModelSerializer):

    founder = serializers.StringRelatedField()
    members = UsernameField(many=True)
    
    class Meta:
        model  = Space
        fields = ['founder', 'name', 'serial', 'members']

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