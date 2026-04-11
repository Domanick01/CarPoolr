from django.conf import settings
from django.db import models


class Ride(models.Model):


    CATEGORY_CHOICES = [
        ('theme_park', 'Theme Park'),
        ('sports', 'Sports Game'),
        ('concert', 'Concert'),
        ('school', 'School'),
        ('other', 'Other'),
    ]

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides",
    )
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    price = models.DecimalField(max_digits=8, decimal_places=2)
    departure_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=4)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["departure_time", "created_at"]

    def __str__(self) -> str:
        return f"{self.pickup_location} → {self.destination} @ {self.departure_time}"
    
    def seats_taken(self):
        """Number of accepted RideRequests"""
        return self.requests.filter(status='accepted').count()  # use 'requests' here

    def seats_available(self):
        """Remaining seats"""
        return max(self.total_seats - self.seats_taken(), 0)

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ride_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ride', 'passenger']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.passenger.username} → {self.ride} ({self.status})"
