from rest_framework import serializers
from db_connection.models import flocculation_data, bsf_data
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class flocdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = flocculation_data
        fields = [
            "url",
            "surface_water",
            "initial_pH",
            "initial_EC",
            "initial_turbidity",
            "flocculant",
            "floc_dose",
            "floc_concentration",
            "floc_saline_Molarity",
            "floc_cactus_share",
            "floc_vol",
            "saline_concentration",
            "final_pH",
            "final_EC",
            "final_turbidity",
            "cal_final_EC",
            "delta_EC",
            "stirring_speed_coagulation_phase",
            "duration_coagulation_phase",
            "stirring_speed_flocculation_phase",
            "duration_flocculation_phase",
            "duration_sedimentation_phase"]

class bsfdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bsf_data
        fields = [
            "url",
            "diameter",
            "material",
            "material_height",
            "min_grain_diameter",
            "max_grain_diameter",
            "mean_grain_diameter",
            "min_flow",
            "max_flow",
            "mean_flow",
            "min_pause",
            "max_pause",
            "mean_pause",
            "time_schmutzdecke",
            "initial_ecoli",
            "final_ecoli",
            "initial_turbidity",
            "final_turbidity"]