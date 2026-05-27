from django import forms
from .models import Reservation
from datetime import date, time

class Step1Form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["pickup_location", "dropoff_location", "pickup_date", "pickup_time", "passengers"]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class Step3Form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["first_name", "last_name", "email", "phone_number", "payment_method"]
        widgets = {
            "payment_method": forms.RadioSelect()
        }