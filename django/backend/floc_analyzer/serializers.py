from rest_framework import serializers
from floc_analyzer.models import addTwoNumberData


class TwoNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = addTwoNumberData
        fields = ['firstnum', 'secondnum']