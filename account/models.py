from django.db import models

# Fields: First Name: String, Last Name: String, Age: Integer, Driver Status: Boolean,
# Verification Status: Boolean, Rating: Float, Car: object
class User(models.Model):
    FIRST_NAME = models.CharField(max_length=100)
    LAST_NAME = models.CharField(max_length=100)
    Username = models.CharField(max_length=100)
    Age = models.IntegerField()
    Email = models.EmailField()
    Phone_Number = models.IntegerField()
    Driver_Status = models.BooleanField(default=False)
    Verified_Status = models.BooleanField(default=False)
    Rating = models.FloatField()

class Car(models.Model):
    CAR_MAKE = models.CharField(max_length=100)
    CAR_MODEL = models.CharField(max_length=100)
