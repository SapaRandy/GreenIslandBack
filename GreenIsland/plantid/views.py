from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import requests
import os
from .firebase import db
from dotenv import load_dotenv
from .plant_utils import scrap_plant, insert_plant_in_firestore

load_dotenv()
PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"
PLANTNET_API_KEY = os.getenv('PLANET_API_KEY')

METEO_API_KEY = os.getenv('METEO_API_KEY')

class UserDeviceListView(APIView):
    def post(self,request):
        userid = request.data.get('userId')
        try:
            results = (db.collection("devices")
                       .where("status", "==", "active")
                       .where("userId","==",userid)
                       .stream())

            devices_without_plantid = [
                doc.id for doc in results
                if 'plantId' not in doc.to_dict()
            ]
            return Response(devices_without_plantid, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PlantConnectView(APIView):
    def post(self, request):
        try:
            db.collection("devices").document(request.data.get("uniqueID")).update({
                'plantId':request.data.get("plantId")
            })
            db.collection("plants").document(request.data.get("plantId")).update({
                'deviceId':request.data.get("uniqueID")
            })

            return Response(status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class PlantIdentifyView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Aucune image fournie.'}, status=400)

        files = {'images': (image_file.name, image_file, image_file.content_type)}
        params = {'api-key': PLANTNET_API_KEY}
        response = requests.post(PLANTNET_API_URL, files=files, params=params)

        if response.status_code != 200:
            return Response({'error': 'Erreur API Pl@ntNet.'}, status=500)

        data = response.json()
        try:
            best_match = data['results'][0]['species']['scientificNameWithoutAuthor']
        except (KeyError, IndexError):
            best_match = None

        return Response({'plant_name': best_match})

class PlantScrapAPIView(APIView):
    def get(self, request, *args, **kwargs):

        name = request.query_params.get('name').lower()
        words = name.split()
        if not name:
            return Response({"error": "Paramètre 'name' manquant."}, status=400)
        try:
            for word in words:
                doc_ref = db.collection('plants_data').document(word)
                doc = doc_ref.get()
                if doc.exists:
                    return Response(doc.to_dict())
                texte = scrap_plant(word)
                if texte:
                    insert_plant_in_firestore({"plant": word, "texte": texte})
                    return Response({"plant": word, "data": texte})

            doc_ref = db.collection('plants_data').document(name)
            doc = doc_ref.get()
            if doc.exists:
                return Response(doc.to_dict())
            texte = scrap_plant(name)
            if texte:
                insert_plant_in_firestore({"plant": name, "texte": texte})
                return Response({"plant": name, "data": texte})
            return Response({"error": "Aucun texte trouvé."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class WeatherAPIView(APIView):
    def get(self, request, *args, **kwargs):
        ville = request.GET.get('ville')
        if not ville:
            return Response({'error': 'Paramètre "ville" manquant.'}, status=400)

        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': ville,
            'appid': METEO_API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            return Response(weather_data)
        else:
            return Response({'error': 'Ville non trouvée ou erreur API.'}, status=response.status_code)


class WeatherWeekAPIView(APIView):
    def get(self, request, *args, **kwargs):
        ville = request.GET.get('ville')
        if not ville:
            return Response({'error': 'Paramètre "ville" manquant.'}, status=400)

        geo_url = 'http://api.openweathermap.org/geo/1.0/direct'
        geo_params = {'q': ville, 'appid': METEO_API_KEY}
        try:
            geo_resp = requests.get(geo_url, params=geo_params,timeout=5)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if not geo_data:
                return Response({'error': 'Ville non trouvée.'}, status=404)
            lat = geo_resp.json()[0]['lat']
            lon = geo_resp.json()[0]['lon']
        except requests.RequestException:
            return Response({'error': 'Erreur de connexion à l\'API de géocodage.'},
                            status=503)

        url = 'https://api.openweathermap.org/data/3.0/onecall'
        params = {
            'lat': lat,
            'lon': lon,
            'exclude': 'minutely,hourly,alerts',
            'appid': METEO_API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return Response(data.get('daily',[]), status= 200)
        except requests.RequestException:
            return Response({'error': 'Erreur API météo.'}, status=503)