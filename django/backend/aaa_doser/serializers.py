from rest_framework import serializers
from aaa_doser.models import predictAAAData

class predictAAASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictAAAData
        fields = ["contact_time", "concentration"]
