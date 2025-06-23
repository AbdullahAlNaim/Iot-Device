from rest_framework import serializers
from .models import Device, Payload
import base64

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

from rest_framework import serializers
from .models import Device, Payload
import base64

class PayloadSerializer(serializers.ModelSerializer):
    devEUI = serializers.CharField(write_only=True)

    class Meta:
        model = Payload
        fields = ['devEUI', 'fcnt', 'data', 'rx_info', 'tx_info', 'status']
        read_only_fields = ['status']

    def to_internal_value(self, data):
        # Translate camelCase to snake_case before validation
        data = data.copy()
        if 'fCnt' in data:
            data['fcnt'] = data.pop('fCnt')
        if 'rxInfo' in data:
            data['rx_info'] = data.pop('rxInfo')
        if 'txInfo' in data:
            data['tx_info'] = data.pop('txInfo')
        return super().to_internal_value(data)

    def validate(self, attrs):
        dev_eui = attrs.get('devEUI')
        fcnt = attrs.get('fcnt')

        try:
            device = Device.objects.get(dev_eui=dev_eui)
        except Device.DoesNotExist:
            device = Device.objects.create(dev_eui=dev_eui)

        attrs['device'] = device

        if Payload.objects.filter(device=device, fcnt=fcnt).exists():
            raise serializers.ValidationError("Duplicate fCnt for this device.")

        data_b64 = attrs.get('data')

        if data_b64:
            try:
                decoded_bytes = base64.b64decode(data_b64)
            except:
                raise serializers.ValidationError({'data': 'Invalid base64-encoded data.'})

            data_hex = decoded_bytes.hex()
            attrs['data'] = data_hex
            attrs['status'] = 'passing' if data_hex == '01' else 'failing'

        return attrs

    def create(self, validated_data):
        validated_data.pop('devEUI')  # Remove because it's not a model field
        payload = super().create(validated_data)

        device = payload.device
        device.last_status = payload.status
        device.save()

        return payload

