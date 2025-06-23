from django.test import TestCase
from devices.models import Device, Payload

class TestBase(TestCase):
    def setUp(self):
        self.device_data = {
            'device_name':'Device 1',
            'dev_eui':'abcdabcdabcdabcd',
            'last_status':'passing'
        }

        self.device = Device.objects.create(**self.device_data)  

        self.payload_data = {
            "device": self.device,
            "fcnt": 100,
            "data": "AQ==",
            "status": "passing",
            "rx_info": {
                "gatewayID": "1234123412341234",
                "name": "G1",
                "time": "2022-07-19T11:00:00",
                "rssi": -57,
                "loRaSNR": 10
            },
            "tx_info": {
                "frequency": 86810000,
                "dr": 5
            }
        }

        self.payload = Payload.objects.create(**self.payload_data)

