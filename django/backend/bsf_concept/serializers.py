from rest_framework import serializers
from bsf_concept.models import predictBsfData, optimizeBsfData

class predictBsfSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictBsfData
        fields = [
            "print_assessment",
            "load_pipe",
            "diameter",
            "material_height",
            "mean_grain_diameter",
            "mean_flow",
            "mean_pause",
            "time_schmutzdecke",
            "initial_turbidity"
        ]


class optimizeBsfSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = optimizeBsfData
        fields = [
            "print_assessment", "load_pipe",
            "diameter_min", "diameter_max",
            "material_height_min", "material_height_max",
            "mean_grain_diameter_min", "mean_grain_diameter_max",
            "mean_flow_min", "mean_flow_max",
            "mean_pause_min", "mean_pause_max",
            "time_schmutzdecke_min", "time_schmutzdecke_max",
            "initial_turbidity_min", "initial_turbidity_max"
        ]