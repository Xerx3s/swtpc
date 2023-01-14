from django.db import models
from floc_analyzer.scripts.modules.connectdb import connectdb

def get_sw():
    df = connectdb().flocdatatodf()
    sw_list = df["surface_water"].unique().tolist()
    sw = []
    for entry in sw_list:
        sw.append((entry, entry))
    return sw

def get_floc():
    df = connectdb().flocdatatodf()
    floc_list = df["flocculant"].unique().tolist()
    floc = []
    for entry in floc_list:
        floc.append((entry, entry))
    return floc

class predictECData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    initial_EC = models.IntegerField(blank=False, default="400")
    floc_concentration = models.FloatField(blank=False, default="20")
    floc_saline_Molarity = models.FloatField(blank=False, default="0.3")
    floc_dose = models.IntegerField(blank=False, default="200")

class predictpHData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    initial_pH = models.FloatField(blank=False, default="8.5")
    floc_concentration = models.FloatField(blank=False, default="20")
    floc_saline_Molarity = models.FloatField(blank=False, default="0.3")
    floc_dose = models.IntegerField(blank=False, default="200")

class predictTurData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    surface_water = models.CharField(max_length=50, blank=False, choices=get_sw())
    initial_pH = models.FloatField(blank=False, default="8.5")
    initial_EC = models.IntegerField(blank=False, default="400")
    initial_turbidity = models.IntegerField(blank=False, default="135")
    flocculant = models.CharField(max_length=50, blank=False, choices=get_floc())
    floc_saline_Molarity = models.FloatField(blank=False, default="0.3")
    floc_dose = models.IntegerField(blank=False, default="200")
    floc_cactus_share = models.IntegerField(blank=False, default="0")
    stirring_speed_coagulation_phase = models.IntegerField(blank=False, default="100")
    duration_coagulation_phase = models.IntegerField(blank=False, default="1")
    stirring_speed_flocculation_phase = models.IntegerField(blank=False, default="20")
    duration_flocculation_phase = models.IntegerField(blank=False, default="15")
    duration_sedimentation_phase = models.IntegerField(blank=False, default="45")