from django.urls import path, include
from .views import DeviceViewSet, PayloadViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'payloads', PayloadViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('api/', include(router.urls))
]
