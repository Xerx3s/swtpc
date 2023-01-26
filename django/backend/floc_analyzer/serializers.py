from rest_framework import serializers
from floc_analyzer.models import predictECData, predictpHData, predictTurData, optimizeTurData

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

class optimizeTurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = optimizeTurData
        fields = [
            "print_assessment", "load_pipe", "pred_type", "flocculant", "surface_water",
            "initial_pH_min", "initial_pH_max",
            "initial_EC_min", "initial_EC_max",
            "initial_turbidity_min", "initial_turbidity_max",
            "floc_concentration_min", "floc_concentration_max",
            "floc_saline_Molarity_min", "floc_saline_Molarity_max",
            "floc_dose_min", "floc_dose_max",
            "floc_cactus_share_min", "floc_cactus_share_max",
            "stirring_speed_coagulation_phase_min", "stirring_speed_coagulation_phase_max",
            "duration_coagulation_phase_min", "duration_coagulation_phase_max",
            "stirring_speed_flocculation_phase_min", "stirring_speed_flocculation_phase_max",
            "duration_flocculation_phase_min", "duration_flocculation_phase_max",
            "duration_sedimentation_phase_min", "duration_sedimentation_phase_max",
        ]