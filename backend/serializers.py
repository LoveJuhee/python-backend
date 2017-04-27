from rest_framework import serializers
from backend.models import Sensor, Center


class CenterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Center
        fields = ('id', 'name', 'label', 'address',
                  'created_at', 'modified_at',)


class SensorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'name', 'model', 'serialnumber',
                  'created_at', 'modified_at',)
