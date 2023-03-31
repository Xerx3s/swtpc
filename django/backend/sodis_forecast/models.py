from django.db import models

class SODISForecastData(models.Model):
    latitude = models.FloatField(blank=False, default="0.0")
    longitude = models.FloatField(blank=False, default="0.0")
    starting_hour = models.IntegerField(blank=False, default="8")
    water_temperature = models.IntegerField(blank=False, default="18")
    target_logdis = models.IntegerField(blank=False, default="4")