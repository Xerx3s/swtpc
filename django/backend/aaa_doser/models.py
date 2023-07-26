from django.db import models
from aaa_doser.scripts.modules.connectdb import connectdb

class predictAAAData(models.Model):
    concentration = models.FloatField(blank=False, default="5")
    contact_time = models.FloatField(blank=False, default="10")
    concentration_chloride = models.FloatField(blank=False, default="0")
    concentration_sulfate = models.FloatField(blank=False, default="0")
    concentration_bicarbonate = models.FloatField(blank=False, default="0")
    concentration_hydrogen_phosphate = models.FloatField(blank=False, default="0")
    concentration_arsenic = models.FloatField(blank=False, default="0")