from django.db import models

class SODISForecastData(models.Model):
    location_city = models.CharField(blank=False, max_length=50, default="Darmstadt")
    location_country = models.CharField(blank=False, max_length=50, default="Deutschland")
    starting_hour = models.IntegerField(blank=False, default="8")
    water_temperature = models.IntegerField(blank=False, default="18")
    target_logdis = models.IntegerField(blank=False, default="4")