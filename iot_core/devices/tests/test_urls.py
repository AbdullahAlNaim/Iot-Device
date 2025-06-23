from django.test import TestCase
from django.urls import reverse, resolve
from devices.views import DeviceViewSet, PayloadViewSet

class TestUrls(TestCase):

    def test_list_urls_is_resolved(self):
        url = reverse('device-list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.cls, DeviceViewSet)

    def test_devices_detail_url_resolves(self):
        url = reverse('device-detail', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.cls, DeviceViewSet)

    def test_payload_urls_is_resolve(self):
        url = reverse('payload-list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.cls, PayloadViewSet)

    def test_payload_detail_url_resolves(self):
        url = reverse('payload-detail', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.cls, PayloadViewSet)
