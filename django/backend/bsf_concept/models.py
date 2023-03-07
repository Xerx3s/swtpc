from django.db import models
from bsf_concept.scripts.modules.connectdb import connectdb

def get_materials():
    df = connectdb().bsfdatatodf()
    materials_list = df["material"].unique().tolist()
    materials = []
    for entry in materials_list:
        materials.append((entry, entry))
    return materials

def get_bounds():
    df = connectdb().bsfdatatodf()
    df.drop(labels=[
        "id", "material", "final_turbidity",
        "min_grain_diameter", "max_grain_diameter",
        "min_flow", "max_flow",
        "min_pause", "max_pause",
        "initial_ecoli", "final_ecoli",
    ], axis=1, inplace=True)
    lb = df.min()
    ub = df.max()
    bounds = {}
    for index,value in lb.items():
        bounds[index] = [value, ub[index]+0.1]
    return bounds

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

class optimizeBsfData(models.Model):
    print_assessment = models.BooleanField(blank=False, default=False)
    load_pipe = models.BooleanField(blank=False, default=False)
    diameter_min = models.IntegerField(blank=False, default="30")
    diameter_max = models.IntegerField(blank=False, default="30")
    material_height_min = models.FloatField(blank=False, default="10")
    material_height_max = models.FloatField(blank=False, default="10")
    mean_grain_diameter_min = models.FloatField(blank=False, default="0.3")
    mean_grain_diameter_max = models.FloatField(blank=False, default="0.3")
    mean_flow_min = models.FloatField(blank=False, default="10")
    mean_flow_max = models.FloatField(blank=False, default="10")
    mean_pause_min = models.IntegerField(blank=False, default="24")
    mean_pause_max = models.IntegerField(blank=False, default="24")
    time_schmutzdecke_min = models.IntegerField(blank=False, default="14")
    time_schmutzdecke_max = models.IntegerField(blank=False, default="14")
    initial_turbidity_min = models.IntegerField(blank=False, default="50")
    initial_turbidity_max = models.IntegerField(blank=False, default="50")