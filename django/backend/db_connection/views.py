from rest_framework import viewsets, permissions
from db_connection.models import flocculation_data, bsf_data, aaa_data
from db_connection.serializers import flocdataSerializer, bsfdataSerializer, aaadataSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class flocdataViewSet(viewsets.ModelViewSet):
    queryset = flocculation_data.objects.all()
    serializer_class = flocdataSerializer
    #permission_classes = [permissions.IsAuthenticated]

class bsfdataViewSet(viewsets.ModelViewSet):
    queryset = bsf_data.objects.all()
    serializer_class = bsfdataSerializer
    #permission_classes = [permissions.IsAuthenticated]

class aaadataViewSet(viewsets.ModelViewSet):
    queryset = aaa_data.objects.all()
    serializer_class = aaadataSerializer
    #permission_classes = [permissions.IsAuthenticated]