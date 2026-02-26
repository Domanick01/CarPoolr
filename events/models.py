from django.db import models
from location_field.models.plain import PlainLocationField

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = PlainLocationField(based_fields='address', zoom=7)
    date = models.DateField()
    start_time = models.TimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

