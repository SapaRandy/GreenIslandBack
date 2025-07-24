from .firebase import db
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_document_name_by_field(collection_name,field_name,field_value):
    docs = (db.collection(collection_name)
             .where(field_name, '==', field_value)
             .stream())

    for doc in docs:
        return doc.id  # On renvoie le nom/ID du premier document trouvé

    return None  # Aucun document trouvé


def get_watering_info_from_plant_doc(plant_doc_id):
    plant_ref = db.collection('plants').document(plant_doc_id).get()
    if not plant_ref.exists:
        message = f"Le document plants/{plant_doc_id} n'existe pas."
        logger.warning(message)
        return None, message

    plant_data = plant_ref.to_dict()
    plant_name = plant_data.get('plantId')
    if not plant_name:
        message = f"Le champ 'name' est manquant dans plants/{plant_doc_id}."
        logger.warning(message)
        return None, message
    logger.info(f"Plante trouvée : {plant_name}")

    plant_data_doc = db.collection("plants_data").document(plant_name).get()
    if not plant_data_doc.exists:
        message = f"Le document plants_data/{plant_name} n'existe pas."
        logger.warning(message)
        return None, message

    plant_data_dict = plant_data_doc.to_dict()
    zone_culture_phrase = plant_data_dict.get('data', {}).get('Zone de Culture', '')
    if not zone_culture_phrase:
        message = f"Zone de culture non trouvée pour la plante '{plant_name}'."
        logger.warning(message)
        return None, message

    logger.info(f"Zone de culture : {zone_culture_phrase}")
    import re
    zone_code_match = re.findall(r'\b\d+[a-zA-Z]*\b', zone_culture_phrase)
    if not zone_code_match:
        message = f"Aucune zone détectée dans la phrase '{zone_culture_phrase}'."
        logger.warning(message)
        return None, message

    zone_code = zone_code_match[0]
    logger.info(f"Code zone extrait : {zone_code}")

    zone_doc = db.collection("zones").document(zone_code).get()
    if not zone_doc.exists:
        message = f"Aucune zone trouvée avec le nom : {zone_code}"
        logger.warning(message)
        return None, message

    zone_data = zone_doc.to_dict()
    watering_info = zone_data.get("watering")
    if not watering_info:
        message = f"Champ 'watering' non trouvé dans la zone '{zone_code}'."
        logger.warning(message)
        return None, message
    logger.info(f"Infos d’arrosage : {watering_info}")

    if watering_info == "medium":
        return 55,None
    elif watering_info == "low":
        return 45,None
    elif watering_info == "high":
        return 65,None