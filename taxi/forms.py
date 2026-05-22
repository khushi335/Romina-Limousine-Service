from django import forms
from .models import Reservation,CarReservation

class CarReservationForm(forms.ModelForm):
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    drop_off_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control'
    }))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'type': 'time',
        'class': 'form-control'
    }))
    drop_off_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'type': 'time',
        'class': 'form-control'
    }))

    class Meta:
        model = CarReservation
        fields = [
            'car_type', 
            'pick_up_location', 
            'drop_off_location', 
            'pick_up_date', 
            'pick_up_time', 
            'drop_off_date', 
            'drop_off_time',
            'email',
            'phone_number',
        ]
        widgets = {
            'car_type': forms.Select(attrs={'class': 'form-select'}),
            'pick_up_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pick Up Location'}),
            'drop_off_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drop Off Location'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
        }
        
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"