from django.urls import path
from .arduinoviews import *

urlpatterns = [
    path('sensor/', ArduinoDataView.as_view(), name='arduino-infos'),
    path('waterpump/', WaterPumpView.as_view(), name='water-pump'),
    path('init/', ArduinoInit.as_view(), name='init'),
    path('connect/', ArduinoConnect.as_view(), name='init'),
]
