from rest_framework import serializers
from user.models import Account


class UsernameField(serializers.RelatedField):
    queryset = Account.objects.all()
    def to_representation(self, value):
        return value.username
    
class AccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    
    class Meta:
        model  = Account
        fields = ('username','password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user