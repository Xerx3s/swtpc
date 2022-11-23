"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import rest_framework
from django.contrib.auth.models import User
from db_connection.models import testtable, flocculation_data
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class testSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = testtable
        fields = ['Name', 'Address', 'Date']

class testViewSet(viewsets.ModelViewSet):
    queryset = testtable.objects.all()
    serializer_class = testSerializer

class flocdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = flocculation_data
        fields = [
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

class flocdataViewSet(viewsets.ModelViewSet):
    queryset = flocculation_data.objects.all()
    serializer_class = flocdataSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tests', testViewSet)
router.register(r'flocdata', flocdataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
