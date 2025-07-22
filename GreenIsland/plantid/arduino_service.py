from .firebase import db
import re

def get_document_name_by_field(collection_name,field_name,field_value):
    docs = (db.collection(collection_name)
             .where(field_name, '==', field_value)
             .stream())

    for doc in docs:
        return doc.id  # On renvoie le nom/ID du premier document trouvé

    return None  # Aucun document trouvé


def get_watering_info_from_plant_doc(plant_doc_id):
    # Étape 1 : Récupérer le document dans la collection "plants"
    plant_ref = db.collection('plants').document(plant_doc_id).get()
    if not plant_ref.exists:
        print("Le document plantes n'existe pas.")
        return None

    plant_data = plant_ref.to_dict()
    plant_name = plant_data.get('name')
    if not plant_name:
        print("Le champ 'name' est manquant dans le document de la plante.")
        return None

    # Étape 2 : Récupérer le document dans "plants_data" en utilisant ce nom
    plant_data_doc = db.collection("plants_data").document(plant_name).get()
    if not plant_data_doc.exists:
        print("Le document correspondant dans 'plants_data' n'existe pas.")
        return None

    plant_data_dict = plant_data_doc.to_dict()
    # Accès à "data" > "zone culture"
    zone_culture_phrase = plant_data_dict.get('data', {}).get('zone culture', '')
    if not zone_culture_phrase:
        print("Zone de culture non trouvée.")
        return None

    # Étape 3 : Extraire le premier mot qui commence par un chiffre
    zone_code_match = re.findall(r'\b\d+[a-zA-Z]*\b', zone_culture_phrase)
    if not zone_code_match:
        print("Aucune zone détectée dans la phrase.")
        return None

    zone_code = zone_code_match[0]

    # Étape 4 : Rechercher dans la collection "zones" le document avec ce nom (par exemple "9b")
    zone_doc = db.collection("zones").document(zone_code).get()
    if not zone_doc.exists:
        print(f"Aucune zone trouvée avec le nom : {zone_code}")
        return None

    zone_data = zone_doc.to_dict()
    watering_info = zone_data.get("watering")
    if not watering_info:
        print("Champ 'watering' non trouvé.")
        return None

    return watering_info