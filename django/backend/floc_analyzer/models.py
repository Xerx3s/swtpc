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

def get_bounds():
    df = connectdb().flocdatatodf()
    df.drop(labels=[
        "id", "surface_water", "flocculant",
        "cal_final_EC", "delta_EC", "final_EC",
        "final_pH", "final_turbidity"], axis=1, inplace=True)
    lb = df.min()
    ub = df.max()
    bounds = {}
    for index,value in lb.items():
        bounds[index] = [value, ub[index]+0.1]
    return bounds
    

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

class optimizeTurData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    pred_type = models.CharField(max_length=3, blank=False, choices=[("ec", "ec"), ("ph", "ph"), ("tur", "tur")])
    surface_water = models.CharField(max_length=50, blank=False, choices=get_sw())
    initial_pH_min = models.FloatField(blank=False, default="8.5")
    initial_pH_max = models.FloatField(blank=False, default="8.5")
    initial_EC_min = models.IntegerField(blank=False, default="400")
    initial_EC_max = models.IntegerField(blank=False, default="400")
    initial_turbidity_min = models.IntegerField(blank=False, default="135")
    initial_turbidity_max = models.IntegerField(blank=False, default="135")
    flocculant = models.CharField(max_length=50, blank=False, choices=get_floc())
    floc_concentration_min = models.IntegerField(blank=False, default="20")
    floc_concentration_max = models.IntegerField(blank=False, default="20")
    floc_saline_Molarity_min = models.FloatField(blank=False, default="0.3")
    floc_saline_Molarity_max = models.FloatField(blank=False, default="0.3")
    floc_dose_min = models.IntegerField(blank=False, default="200")
    floc_dose_max = models.IntegerField(blank=False, default="200")
    floc_cactus_share_min = models.IntegerField(blank=False, default="0")
    floc_cactus_share_max = models.IntegerField(blank=False, default="0")
    stirring_speed_coagulation_phase_min = models.IntegerField(blank=False, default="100")
    stirring_speed_coagulation_phase_max = models.IntegerField(blank=False, default="100")
    duration_coagulation_phase_min = models.IntegerField(blank=False, default="1")
    duration_coagulation_phase_max = models.IntegerField(blank=False, default="1")
    stirring_speed_flocculation_phase_min = models.IntegerField(blank=False, default="20")
    stirring_speed_flocculation_phase_max = models.IntegerField(blank=False, default="20")
    duration_flocculation_phase_min = models.IntegerField(blank=False, default="15")
    duration_flocculation_phase_max = models.IntegerField(blank=False, default="15")
    duration_sedimentation_phase_min = models.IntegerField(blank=False, default="45")
    duration_sedimentation_phase_max = models.IntegerField(blank=False, default="45")