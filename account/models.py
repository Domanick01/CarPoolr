from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Fields: First Name: String, Last Name: String, Age: Integer, Driver Status: Boolean,
# Verification Status: Boolean, Rating: Float, Car: object
class User(models.Model):
    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    Username = models.CharField(max_length=100)
    Age = models.IntegerField()
    Email = models.EmailField()
    Phone_Number = PhoneNumberField(unique=True, blank=True, null=True)
    Driver_Status = models.BooleanField(default=False)
    Verified_Status = models.BooleanField(default=False)
    Rating = models.FloatField()

    def __str__(self):
        return f"{self.FIRST_NAME} {self.LAST_NAME}"

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
