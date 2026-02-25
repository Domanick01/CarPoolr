from django import forms

from .models import Ride


class RideForm(forms.ModelForm):
    departure_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Ride
        fields = ["pickup_location", "destination", "price", "departure_time"]