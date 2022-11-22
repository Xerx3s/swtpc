from django.db import models

class testtable(models.Model):
    Name = models.CharField(max_length=70, blank=False, default='')
    Address = models.CharField(max_length=200,blank=False, default='')
    Date = models.DateField(default='')

class flocculation_data(models.Model):
    surface_water = models.CharField(max_length=50, blank=False, default='')
    initial_pH = models.CharField(max_length=50, blank=False, default='')
    initial_EC = models.CharField(max_length=50, blank=False, default='')
    initial_turbidity = models.CharField(max_length=50, blank=False, default='')
    flocculant = models.CharField(max_length=50, blank=False, default='')
    floc_dose = models.CharField(max_length=50, blank=False, default='')
    concentration = models.CharField(max_length=50, blank=False, default='')
    saline_Molarity = models.CharField(max_length=50, blank=False, default='')
    cactus_share = models.CharField(max_length=50, blank=False, default='')
    floc_vol = models.CharField(max_length=50, blank=False, default='')
    saline_concentration = models.CharField(max_length=50, blank=False, default='')
    final_pH = models.CharField(max_length=50, blank=False, default='')
    final_EC = models.CharField(max_length=50, blank=False, default='')
    final_turbidity = models.CharField(max_length=50, blank=False, default='')
    cal_final_EC = models.CharField(max_length=50, blank=False, default='')
    delta_EC = models.CharField(max_length=50, blank=False, default='')
    stirring_speed_coagulation_phase = models.CharField(max_length=50, blank=False, default='')
    duration_coagulation_phase = models.CharField(max_length=50, blank=False, default='')
    stirring_speed_flocculation_phase = models.CharField(max_length=50, blank=False, default='')
    duration_flocculation_phase = models.CharField(max_length=50, blank=False, default='')
    duration_sedimentation_phase = models.CharField(max_length=50, blank=False, default='')