from django.urls import path
from .views import *
from .arduinoviews import *

urlpatterns = [
    path('identify/', PlantIdentifyView.as_view(), name='identify-plant'),
    path('infos/', PlantScrapAPIView.as_view(), name='plant-info'),
    path('meteo/', WeatherAPIView.as_view(), name='meteo'),
    path('meteosemaine/', WeatherWeekAPIView.as_view(), name='meteo-week'),
]
