from devices.tests.test_setup import TestBase
from devices.serializers import DeviceSerializer, PayloadSerializer


class TestSerializer(TestBase):

    def test_device_serialize_passing(self):
        new_device_data = {
            'device_name': 'Device 2',
            'dev_eui': 'abcdabcdabcdaefg',
            'last_status': 'passing'
        }

        serializer = DeviceSerializer(data=new_device_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['dev_eui'], 'abcdabcdabcdaefg')

    def test_duplicate_fcnt_error(self):
        duplicate_data = self.payload_data.copy()
        duplicate_data['devEUI'] = self.device.dev_eui
        duplicate_data.pop('device', None)  # remove 'device' key if present

        serializer = PayloadSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('Duplicate fCnt for this device.', serializer.errors['non_field_errors'][0])

    def test_payload_base64_to_hexadecimal_status_passing(self):
        new_payload_data = self.payload_data.copy()
        new_payload_data['devEUI'] = self.device.dev_eui
        new_payload_data['fcnt'] = 200
        new_payload_data.pop('device', None)

        serializer = PayloadSerializer(data=new_payload_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['data'], '01')
        self.assertEqual(serializer.validated_data['status'], 'passing')

    def test_payload_invalid_base64_data(self):
        invalid_payload_data = self.payload_data.copy()
        invalid_payload_data['devEUI'] = self.device.dev_eui
        invalid_payload_data['fcnt'] = 201
        invalid_payload_data['data'] = "INVALID!!"
        invalid_payload_data.pop('device', None)

        serializer = PayloadSerializer(data=invalid_payload_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('data', serializer.errors)
        self.assertIn('Invalid base64-encoded data.', serializer.errors['data'][0])

    def test_payload_base64_to_hexadecimal_status_failing(self):
        new_payload_data = self.payload_data.copy()
        new_payload_data['devEUI'] = self.device.dev_eui
        new_payload_data['fcnt'] = 202
        new_payload_data['data'] = 'Ag=='  # base64 of 0x02
        new_payload_data.pop('device', None)

        serializer = PayloadSerializer(data=new_payload_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['data'], '02')
        self.assertEqual(serializer.validated_data['status'], 'failing')
