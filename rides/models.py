from django.conf import settings
from django.db import models


class Ride(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides",
    )
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    departure_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["departure_time", "created_at"]

    def __str__(self) -> str:
        return f"{self.pickup_location} → {self.destination} @ {self.departure_time}"
