from devices.tests.test_setup import TestBase
from django.db import IntegrityError
from devices.models import Device, Payload
from django.core.exceptions import ValidationError


class TestModel(TestBase):
    def test_device_read_passing(self):
        self.assertEqual(self.device.last_status, 'passing')

    def test_device_last_status_defaults_to_failing(self):
        device = Device.objects.create(device_name="some device", dev_eui="abcdabcdabcdaaaa")
        self.assertEqual(device.last_status, "failing")

    def test_device_str_returns_name(self):
        self.assertEqual(str(self.device), 'Device 1')

    def test_payload_device_connects_dev_eui(self):
        self.assertEqual(self.payload.device.dev_eui, 'abcdabcdabcdabcd')

    def test_payload_read_passing(self):
        self.assertEqual(self.payload.status, 'passing')
        self.assertEqual(self.payload.fcnt, 100)

    def test_payload_unique_fcnt(self):
        with self.assertRaises(IntegrityError):
            Payload.objects.create(**self.payload_data)

    def test_payload_str_returns_dev_eui_fcnt(self):
        self.assertEqual(str(self.payload), 'abcdabcdabcdabcd - fCnt 100')

    def test_deleting_device_deletes_payloads(self):
        self.assertEqual(Payload.objects.count(), 1)
        self.device.delete()
        self.assertEqual(Payload.objects.count(), 0)
    
    def test_dev_eui_max_length_validation(self):
        device = Device(device_name="Test", dev_eui="x" * 40)
        with self.assertRaises(ValidationError):
            device.full_clean()