from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .firebase import db
from firebase_admin import firestore
import requests

class ArduinoInit(APIView):
    def post(self, request):
        uniqueID = request.data.get('uniqueID')
        ip = request.data.get('IP')

        if not uniqueID or not ip:
            return Response({"error": "uniqueID and IP are required."}, status=400)

        doc_ref = db.collection('devices').document(uniqueID)
        doc = doc_ref.get()

        try:
            if doc.exists:
                doc_ref.update({"IP": ip})
                return Response(status=200)
            else:
                db.collection('devices').document(uniqueID).set({
                    "IP" :ip,
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'status': 'free'
                })
                return Response(status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

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
        ARDUINO_IP = "172.20.10.6"  # À adapter

        state = request.data.get('state', 'off')
        if state == 'on':
            url = f"http://{ARDUINO_IP}/on"
        else:
            url = f"http://{ARDUINO_IP}/off"

        try:
            resp = requests.get(url, timeout=2)
            return Response({'result': resp.text})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
