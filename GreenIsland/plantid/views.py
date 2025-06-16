from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import requests

PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"
PLANTNET_API_KEY = "VOTRE_CLE_API"  # Remplacez par votre clé

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
        # Récupérer le nom scientifique de la plante la plus probable
        try:
            best_match = data['results'][0]['species']['scientificNameWithoutAuthor']
        except (KeyError, IndexError):
            best_match = None

        return Response({'plant_name': best_match})