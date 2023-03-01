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
from rest_framework import routers
from db_connection.views import flocdataViewSet, bsfdataViewSet, UserViewSet, GroupViewSet
from floc_analyzer.views import predictEcView, predictPhView, predictTurView, optimizeTurView, list_flocculants, list_surface_waters, list_bounds
from bsf_concept.views import predictBsfView, optimizeBsfView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'flocdata', flocdataViewSet)
router.register(r'bsfdata', bsfdataViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ec/', predictEcView.as_view()),
    path('ph/', predictPhView.as_view()),
    path('tur/', predictTurView.as_view()),
    path('sw/', list_surface_waters.as_view()),
    path('floc/', list_flocculants.as_view()),
    path("bounds/", list_bounds.as_view()),
    path("opt_tur/", optimizeTurView.as_view()),
    path("bsf/", predictBsfView.as_view()),
    path("opt_bsf/", optimizeBsfView.as_view())
]
