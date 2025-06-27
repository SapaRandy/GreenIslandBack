from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .firebase import db


class ArduinoDataView(APIView):
    def post(self, request):
        # Récupère les données envoyées par l'Arduino
        data = {
            "temperature": request.data.get('temperature'),
            "humidite": request.data.get('humidite'),
            "pression": request.data.get('pression'),
            "sol": request.data.get('sol'),
            "niveau_eau": request.data.get('niveau_eau'),
        }

        # Enregistre dans une collection Firestore (par exemple "mesures")
        db.collection('mesures').add(data)

        return Response({'message': 'Données reçues'}, status=200)