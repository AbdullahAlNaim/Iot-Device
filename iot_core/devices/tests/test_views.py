from devices.tests.test_setup import TestBase
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from devices.models import Device, Payload


class Test_DeviceViewSet(TestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", password="abc123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_device_list(self):
        url = reverse('device-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["dev_eui"], self.device.dev_eui)

    def test_create_device(self):
        url = reverse('device-list')
        device_data = self.device_data.copy()
        device_data['dev_eui'] = "1234567890abcdef"
        response = self.client.post(url, device_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Device.objects.count(), 2)

    def test_device_list_requires_auth(self):
        self.client.credentials()  # remove token
        url = reverse('device-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


class Test_PayloadViewSet(TestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", password="abc123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_payload_list(self):
        url = reverse('payload-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['fcnt'], self.payload.fcnt)

    def test_create_payload_passing(self):
        url = reverse('payload-list')
        payload_data = self.payload_data.copy()
        payload_data['devEUI'] = self.device.dev_eui
        payload_data['fcnt'] = 101
        payload_data.pop('device', None)

        response = self.client.post(url, payload_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payload.objects.count(), 2)
        self.assertEqual(response.data["status"], "passing")
        self.device.refresh_from_db()
        self.assertEqual(self.device.last_status, "passing")

    def test_create_payload_failing(self):
        url = reverse('payload-list')
        payload_data = self.payload_data.copy()
        payload_data['devEUI'] = self.device.dev_eui
        payload_data['fcnt'] = 102
        payload_data['data'] = "Ag=="
        payload_data.pop('device', None)

        response = self.client.post(url, payload_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "failing")
        self.device.refresh_from_db()
        self.assertEqual(self.device.last_status, "failing")

    def test_duplicate_fcnt(self):
        url = reverse('payload-list')
        payload_data = self.payload_data.copy()
        payload_data['devEUI'] = self.device.dev_eui
        payload_data.pop('device', None)

        response = self.client.post(url, payload_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)
        self.assertIn("Duplicate fCnt for this device.", response.data["non_field_errors"][0])

    def test_payload_list_requires_auth(self):
        self.client.credentials()  # remove token
        url = reverse('payload-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_device_last_status_updates_with_new_payload(self):
        url = reverse('payload-list')

        passing_payload = self.payload_data.copy()
        passing_payload['devEUI'] = self.device.dev_eui
        passing_payload['fcnt'] = 101
        passing_payload.pop('device', None)

        response1 = self.client.post(url, passing_payload, format='json')
        self.assertEqual(response1.status_code, 201)
        self.device.refresh_from_db()
        self.assertEqual(self.device.last_status, "passing")

        failing_payload = self.payload_data.copy()
        failing_payload['devEUI'] = self.device.dev_eui
        failing_payload['fcnt'] = 200
        failing_payload['data'] = "Ag=="
        failing_payload.pop('device', None)

        response2 = self.client.post(url, failing_payload, format='json')
        self.assertEqual(response2.status_code, 201)
        self.device.refresh_from_db()
        self.assertEqual(self.device.last_status, "failing")
