from django.apps import AppConfig
from django.contrib import admin


class ParkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'park'

    def ready(self):
        from .models import Vehicles, Garages, Booking

        admin.site.register(Vehicles)
        admin.site.register(Garages)
        admin.site.register(Booking)
