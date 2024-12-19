from django.forms import ModelForm

from .models import Booking, Vehicles


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicles
        fields = ['tag_number','year', 'make', 'model', 'over_size']