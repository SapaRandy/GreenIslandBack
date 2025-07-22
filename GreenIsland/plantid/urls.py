from django.urls import path
from .views import *
from .arduino_views import *

urlpatterns = [
    path('identify/', PlantIdentifyView.as_view(), name='identify-plant'),
    path('deviceslist/', UserDeviceListView.as_view(), name='device-list'),
    path('connect/', PlantConnectView.as_view(), name='plant-connect'),
    path('infos/', PlantScrapAPIView.as_view(), name='plant-info'),
    path('meteo/', WeatherAPIView.as_view(), name='meteo'),
    path('meteosemaine/', WeatherWeekAPIView.as_view(), name='meteo-week'),
]
