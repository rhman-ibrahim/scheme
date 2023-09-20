from rest_framework import serializers
from home.models import Widget


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Widget
        fields = ['note', 'card']