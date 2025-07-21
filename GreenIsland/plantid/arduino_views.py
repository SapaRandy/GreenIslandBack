from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from firebase_admin import firestore
import requests
from .arduino_service import *
import os

METEO_API_KEY = os.getenv('METEO_API_KEY')

class ArduinoInitView(APIView):
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


class ArduinoConnectView(APIView):
    def get(self):
        results = db.collection("devices").where("status", "==", "free").stream()
        device_ids = [doc.id for doc in results]
        return Response(device_ids, status=200)

    def post(self,request):
        userid = request.data.get('userid')
        try:
            db.collection("devices").document(request.data.get("uniqueID")).update({
                'status':'active',
                'userId':userid
            })
            return Response(status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ArduinoDataView(APIView):
    def post(self, request):
        uniqueID = request.data.get('uniqueID')
        doc_name = get_document_name_by_field("plants","deviceId",uniqueID)

        if doc_name:
            data = {
                "temperature": request.data.get('temperature'),
                "humidite": request.data.get('humidite'),
                "pression": request.data.get('pression'),
                "sol": request.data.get('sol'),
                "niveau_eau": request.data.get('niveau_eau'),
                "date_heure": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "plantId": doc_name
            }

            db.collection('mesures').add(data)

            return Response({'message': 'Données reçues'}, status=200)
        else:
            return Response({'message': 'Appareil non associé à une plante'},status=500)


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

class AutoWateringView(APIView):
    def post(self,request):
        uniqueID = request.data.get('uniqueID')
        doc_name = get_document_name_by_field("plants", "deviceId", uniqueID)
        if not doc_name:
            return Response({'message': 'Appareil non associé à une plante'}, status=400)

        plant_doc = db.collection("plants").document(doc_name).get()
        if not plant_doc.exists:
            return Response({'message': 'Document plante non trouvé'}, status=404)

        plant_data = plant_doc.to_dict()
        auto_mode = plant_data.get("auto", True)
        if not auto_mode:
            return Response({'message': 'Mode auto désactivé'}, status=400)

        outside_field = plant_data.get("isOutdoor",False)
        if outside_field:
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {
                'lat': 48.9535,
                'lon': 2.3168,
                'appid': METEO_API_KEY,
                'units': 'metric',
                'lang': 'fr'
            }
            try:
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()
            except requests.RequestException as e:
                return Response({'message': 'Erreur lors de la connexion à l’API météo'}, status=503)
            if response.status_code == 200:
                data = response.json()
                weather_main = data['weather'][0]['main']
                if weather_main == "Rain":
                    return Response({'message': 'Pluie attendue, arrosage annulé'},status=409)
            else:
                print(f"Erreur lors de la requête : {response.status_code}")

        watering = get_watering_info_from_plant_doc(doc_name)
        if not watering:
            return Response({'message': 'Impossible de récupérer les données d’arrosage'}, status=503)

        return Response({'watering': watering}, status=200)