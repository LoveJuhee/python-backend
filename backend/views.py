from rest_framework import generics
from backend.models import Sensor, Center
from backend.serializers import SensorSerializer, CenterSerializer


class SensorViewSet(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class CenterViewSet(generics.ListCreateAPIView):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
