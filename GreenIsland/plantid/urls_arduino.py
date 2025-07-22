from django.urls import path
from .arduino_views import *

urlpatterns = [
    path('sensor/', ArduinoDataView.as_view(), name='arduino-infos'),
    path('waterpump/', WaterPumpView.as_view(), name='water-pump'),
    path('init/', ArduinoInitView.as_view(), name='init'),
    path('connect/', ArduinoConnectView.as_view(), name='connect'),
    path('devicelist/', ListUserDevice.as_view(), name='devicelist'),
    path('limit/', AutoWateringView.as_view(), name='limit'),
]
