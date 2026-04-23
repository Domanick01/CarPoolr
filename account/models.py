from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Fields: First Name: String, Last Name: String, Age: Integer, Driver Status: Boolean,
# Verification Status: Boolean, Rating: Float, Car: object
class User(AbstractUser):
    SCHOOL_CHOICES = [
    ('florida_southern', 'Florida Southern College'),
    ('ucf', 'University of Central Florida'),
    ('other', 'Other'),
]

    Age = models.IntegerField(null=True, blank=True)
    Phone_Number = PhoneNumberField(unique=True, blank=True, null=True)
    Driver_Status = models.BooleanField(default=False)
    Verified_Status = models.BooleanField(default=False)
    Rating = models.FloatField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=100, choices=SCHOOL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Car(models.Model):
    CAR_MAKE = models.CharField(max_length=100)
    CAR_MODEL = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.CAR_MAKE} {self.CAR_MODEL}"

    class Meta:
        db_table = 'car'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['CAR_MAKE']
