from django.db import models

class predictBsfData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    diameter = models.IntegerField(blank=False, default="30")
    material_height = models.FloatField(blank=False, default="10")
    mean_grain_diameter = models.FloatField(blank=False, default="0.3")
    mean_flow = models.FloatField(blank=False, default="10")
    mean_pause = models.IntegerField(blank=False, default="24")
    time_schmutzdecke = models.IntegerField(blank=False, default="14")
    initial_turbidity = models.IntegerField(blank=False, default="50")
