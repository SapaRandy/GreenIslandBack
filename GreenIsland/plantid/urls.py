from django.urls import path
from .views import *
from .arduino_views import *

urlpatterns = [
    path('identify/', PlantIdentifyView.as_view(), name='identify-plant'),
    path('connect/', PlantConnectView.as_view(), name='plant-connect'),
    path('connect/<str:userId>/', PlantConnectView.as_view(), name='plant-connect'),
    path('infos/', PlantScrapAPIView.as_view(), name='plant-info'),
    path('mesures/<str:plantId>/', PlantDataAPIView.as_view(), name='mesures'),
    path('meteo/', WeatherAPIView.as_view(), name='meteo'),
    path('meteosemaine/', WeatherWeekAPIView.as_view(), name='meteo-week'),
]
