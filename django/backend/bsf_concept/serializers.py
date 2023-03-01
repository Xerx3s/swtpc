from rest_framework import serializers
from bsf_concept.models import predictBsfData

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
