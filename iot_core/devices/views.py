from .models import Device, Payload
from .serializers import DeviceSerializer, PayloadSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class PayloadViewSet(ModelViewSet):
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

