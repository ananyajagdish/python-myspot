from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Booking(models.Model):
    parking_garage_id = models.IntegerField()
    vehicle_id = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Customer ID: {self.user}\nParking Garage ID: {self.parking_garage_id}\nStart Time: {self.start_time}\nEnd Time: {self.end_time}\nStatus: {self.status}'

    class Meta:
        db_table = 'bookings'

class Vehicles(models.Model):
    tag_number = models.CharField(max_length=25)
    year = models.CharField(max_length=25)
    make = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    over_size = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vehicles'

class Garages(models.Model):
    name  = models.CharField(max_length=50)
    max_capacity = models.IntegerField()
    remaining_capacity = models.IntegerField()
    street_address  = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    postal_code  = models.CharField(max_length=15)

    class Meta:
        db_table = 'garages'

