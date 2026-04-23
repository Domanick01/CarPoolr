from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Location',
        })
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }