from rest_framework import serializers
from sodis_forecast.models import SODISForecastData

class SODISForecastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SODISForecastData
        fields = ['location_city', 'location_country', 'starting_hour', 'water_temperature', 'target_logdis']
