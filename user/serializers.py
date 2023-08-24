from rest_framework import serializers
from user.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Account
        fields = ('username',)


class UsernameField(serializers.RelatedField):
    
    queryset = Account.objects.all()
    
    def to_representation(self, value):
        return value.username