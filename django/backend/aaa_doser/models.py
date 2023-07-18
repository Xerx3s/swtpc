from django.db import models
from aaa_doser.scripts.modules.connectdb import connectdb

class predictAAAData(models.Model):
    concentration = models.FloatField(blank=False, default="5")
    contact_time = models.FloatField(blank=False, default="10")