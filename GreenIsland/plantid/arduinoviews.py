from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from datetime import datetime
from .firebase import db
import requests
from django.http import JsonResponse


class ArduinoDataView(APIView):
    def post(self, request):
        data = {
            "temperature": request.data.get('temperature'),
            "humidite": request.data.get('humidite'),
            "pression": request.data.get('pression'),
            "sol": request.data.get('sol'),
            "niveau_eau": request.data.get('niveau_eau'),
            "date_heure": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        db.collection('mesures').add(data)

        return Response({'message': 'Données reçues'}, status=200)

class WaterPumpView(APIView):
    def post(self, request):
        ARDUINO_IP = "192.168.1.50"  # Remplace par l'IP affichée par ton Arduino

        def pump_control(request):
            state = request.GET.get('state', 'off')
            if state == 'on':
                url = f"http://{ARDUINO_IP}/on"
            else:
                url = f"http://{ARDUINO_IP}/off"
            try:
                resp = requests.get(url, timeout=2)
                return JsonResponse({'result': resp.text})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
