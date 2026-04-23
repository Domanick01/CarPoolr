from django import forms
from .models import Ride, Review


class RideForm(forms.ModelForm):
    departure_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Ride
        fields = ["pickup_location", "destination", "price", "departure_time", "event"]
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }