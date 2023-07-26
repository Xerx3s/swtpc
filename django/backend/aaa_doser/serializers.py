from rest_framework import serializers
from aaa_doser.models import predictAAAData

class predictAAASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = predictAAAData
        fields = ["concentration",
                  "contact_time",
                  "concentration_chloride",
                  "concentration_sulfate",
                  "concentration_bicarbonate",
                  "concentration_hydrogen_phosphate",
                  "concentration_arsenic"]
