from rest_framework import serializers
from db_connection.models import flocculation_data
from django.contrib.auth.models import User, Group
from rest_framework import serializers


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
            "concentration",
            "saline_Molarity",
            "cactus_share",
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