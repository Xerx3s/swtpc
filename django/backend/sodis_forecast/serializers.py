from rest_framework import serializers
from sodis_forecast.models import SODISForecastData

class SODISForecastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SODISForecastData
        fields = ['latitude', 'longitude', 'starting_hour', 'water_temperature', 'target_logdis']
