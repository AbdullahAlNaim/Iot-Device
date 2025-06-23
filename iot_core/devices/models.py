from django.db import models

# Create your models here.

# cleanest and most modern approach for field choices
class StatusChoices(models.TextChoices):
    PASSING = 'passing', 'Passing'
    FAILING = 'failing', 'Failing'


class Device(models.Model):
    device_name = models.CharField(max_length=100, null=True, blank=True)
    dev_eui = models.CharField(max_length=32, unique=True)
    last_status = models.CharField(
         max_length=10,
         choices=StatusChoices.choices,
         default=StatusChoices.FAILING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.device_name or self.dev_eui


class Payload(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='payloads')
    fcnt = models.PositiveIntegerField()
    data = models.CharField(max_length=10)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.FAILING
    )
    rx_info = models.JSONField()
    tx_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('device', 'fcnt')

    def __str__(self):
         return f"{self.device.dev_eui} - fCnt {self.fcnt}"