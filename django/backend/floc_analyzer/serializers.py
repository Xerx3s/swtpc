from rest_framework import serializers
from floc_analyzer.models import predictECData, predictpHData, predictTurData

class predictECSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictECData
        fields = ["print_assessment", "load_pipe", "initial_EC", "floc_concentration", "floc_saline_Molarity", "floc_dose"]

class predictpHSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictpHData
        fields = ["print_assessment", "load_pipe", "initial_pH", "floc_concentration", "floc_saline_Molarity", "floc_dose"]

class predictTurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictTurData
        fields = [
            "print_assessment", "load_pipe", 
            "surface_water", "initial_pH", "initial_EC", "initial_turbidity",
            "flocculant", "floc_saline_Molarity", "floc_dose", "floc_cactus_share",
            "stirring_speed_coagulation_phase", "duration_coagulation_phase",
            "stirring_speed_flocculation_phase", "duration_flocculation_phase",
            "duration_sedimentation_phase"]